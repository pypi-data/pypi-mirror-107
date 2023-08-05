import time
from collections import namedtuple
from importlib.metadata import version
from typing import Dict, Optional

import sanic
import ujson
from sanic import Sanic
from sanic.log import logger
from sanic.response import HTTPResponse
from sanic.request import Request

from qai.util import convert_issue_spans_to_utf16, get_cpu_quota_within_docker
from qai.validation import Validator, filter_no_ops


SegmentWrapper = namedtuple("SegmentWrapper", ["id", "segment", "meta", "category"])


async def set_valid_segments(request: Request):
    """
    uses `request.ctx.validator`, which must already be set,
    to validate segments.
    Stores valid segments to `request.ctx.segments` and also sets `request.ctx.info`

    This is used by default in QRest, or can be used in a standalone sanic app with

    ```python
    from qai.server import set_valid_segments

    ...
    app.request_middleware.append(set_valid_segments)
    ```
    """
    if request.method != "POST":
        return None
    data = request.json
    req = data.get("request", {"segments": []})
    segs = req.get("segments", [])
    # store segments in context
    request.ctx.segments = []
    # store extra info if eventually needed
    info = {k: v for k, v in req.items() if k != "segments"}
    for el in segs:
        s_id = el["content"]["segmentId"]
        segment = el["content"]["segment"]
        meta = el.get("meta", {})
        category = el["category"]
        is_valid = request.app.ctx.validator(segment)
        tpe = el["content"]["tpe"]
        frm = el["content"]["from"]
        if is_valid:
            request.ctx.segments.append(SegmentWrapper(s_id, segment, meta, category))
            info.update(
                {"type": tpe, "from": frm, "segmentId": s_id, "category": category,}
            )
            # jam all non-meta into request.ctx.info
            request.ctx.info = info


async def postprocess_issues(
    request: Request, response: HTTPResponse
) -> Optional[HTTPResponse]:
    """
    THIS MUST BE THE LAST MIDDLEWARE
    since when it works, it returns, which bypasses remaining middleware

    It changes the string indexing to be utf-16 based, and filters no ops
    This is used by default in QRest, or can be used in a standalone sanic app with

    ```python
    from qai.server import postprocess_issues

    ...
    app.response_middleware.append(postprocess_issues)
    ```

    However, if you use your own handler and import this middleware, you must set
    the key "segment" in addition to the 3 standard keys of a response,
    "category", "segmentId", "issues"

    if there is an error, though, it should still respond, since when there is
    an exception in middleware, sanic sends whatever the handler returned
    which in this case is issues which possibly contain no-ops and have the wrong indexing
    """
    if request.method != "POST":
        # don't run on health checks
        return None
    res = ujson.loads(response.body)
    for segment_response in res:
        segment = segment_response["segment"]
        segment_response["issues"] = filter_no_ops(segment, segment_response["issues"])
        del segment_response["segment"]
        if not request.app.ctx.utf16_convert:
            continue
        for i, issue in enumerate(segment_response["issues"]):
            segment_response["issues"][i] = convert_issue_spans_to_utf16(segment, issue)
    # since we return, no other middleware will be run after this
    return sanic.response.json(res)


async def main_handler(request: Request) -> HTTPResponse:
    """
    The default handler, which works when the service responds with one category

    Must come after the middleware which sets request.ctx.analyzer

    If you have to respond with multiple categories it should still work if you
    pass QRest(..., issue_type_to_categories={"some_type": "some_category"})

    Most of the code is just for handling issue_type to category mapping
    """
    it2c = request.app.ctx.issue_type_to_category
    res = []
    for s_id, segment, meta, category in request.ctx.segments:
        issues = request.app.ctx.analyzer(segment, meta, request.ctx.info)
        if it2c is None:
            segment_response = {
                "category": category,
                "segmentId": s_id,
                "segment": segment,
                "issues": issues,
            }
            res.append(segment_response)
        else:
            types = it2c.keys()
            for t in types:
                res.append(
                    {
                        "category": it2c[t],
                        "segmentId": s_id,
                        "segment": segment,
                        "issues": [i for i in issues if i["issueType"] == t],
                    }
                )
    return sanic.response.json(res)


async def get_root(request: Request) -> HTTPResponse:
    return sanic.response.json(request.app.ctx.status_dump)


async def add_start_time(request: Request):
    """Prepend initial time when this request was served."""
    request.ctx.start_time = time.time()


async def add_perf_stats(request: Request, response: HTTPResponse):
    """
    Prepend initial time when this request was served.
    Log the access long on each request.
    Log num of segments, sentences, words in payload.
    Log sentence and word speed.
    """
    is_get = request.method.lower() == "get"
    is_check = request.path in ["/ready", "/healthy"]
    should_log = not (is_get or is_check)
    if not should_log:
        return
    latency = round((time.time() - request.ctx.start_time) * 1000)
    sids = "[" + ", ".join([s.id for s in request.ctx.segments]) + "]"
    logger.info(
        (
            "{method} {url} {status} {latency}ms {reqbytes}reqBytes {resbytes}resBytes"
            " docId={documentId} version={version} segIds={segmentIds}"
        ).format(
            method=request.method,
            url=request.url,
            status=response.status,
            latency=latency,
            reqbytes=len(request.body),
            resbytes=len(response.body),
            documentId=request.ctx.info.get("documentId", -1),
            version=request.ctx.info.get("version", -1),
            segmentIds=sids,
        )
    )


class QRest:
    def __init__(
        self,
        analyzer,
        category: str,
        host: str = "0.0.0.0",
        port: int = 5000,
        workers: Optional[int] = None,
        debug: bool = False,
        ignore_html: bool = True,
        ignore_inside_quotes: bool = False,
        ignore_token_fraction: float = 0.5,
        app: Optional[Sanic] = None,
        issue_type_to_category: Dict[str, str] = None,
        utf16_convert: bool = True,
    ):
        """
        A convenience class for building a class given an Analyzer class

        you can control parameters of the server with host/port/workers/debug
        or, you can pass a Sanic app using the app= kwarg

        If your service handles multiple categories (like punctuation), you must either build the app yourself
        or pass issue_type_to_category, a Dict that maps issue type (str) to category (str)
        """
        self.host = host
        self.port = port
        self.category = category
        self.debug = debug
        self.ignore_html = ignore_html
        self.ignore_inside_quotes = ignore_inside_quotes
        self.validator = Validator(
            ignore_html=ignore_html, ignore_token_fraction=ignore_token_fraction,
        )
        self.analyzer = analyzer
        if not callable(analyzer):
            raise ValueError(
                "Analyzer instance must be callable, with signature (segment, meta=None, extra_info=None)."
            )

        if workers is None:
            self.workers = get_cpu_quota_within_docker()
        else:
            self.workers = int(workers)

        if app is None:
            app = Sanic(__name__)
            app.ctx.issue_type_to_category = issue_type_to_category
            # now the handlers will get called
            app.add_route(main_handler, "/", methods=["POST"])
            app.add_route(main_handler, "/v2", methods=["POST"])
        # I assume even custom-passed apps will want these attached
        app.ctx.validator = self.validator
        app.ctx.analyzer = self.analyzer
        app.ctx.status_dump = {
            "service": self.category,
            "status": "up",
            "host": self.host,
            "port": self.port,
            "qai version": version("qai"),
        }
        app.ctx.utf16_convert = utf16_convert
        # validate segments, attach valid ones to request.ctx
        app.request_middleware.append(set_valid_segments)
        # Add the request and response middleware for logging
        app.request_middleware.append(add_start_time)
        app.response_middleware.append(add_perf_stats)
        # Handlers Run Here
        # middleware to filter no-ops
        # THIS MUST BE THE LAST MIDDLEWARE
        app.response_middleware.append(postprocess_issues)
        # attach and add health check, status routes
        self.app = app
        self.add_simple_routes()

    def add_simple_routes(self):
        self.app.add_route(get_root, "/", methods=["GET"])
        self.app.add_route(get_root, "/ready", methods=["GET"])
        self.app.add_route(get_root, "/healthy", methods=["GET"])

    def get_future(self):
        """
        Return a Future (Promise in JS land) that can be put on an event loop

        You probably don't need this unless you are doing crazy stuff
        """
        return self.app.create_server(host=self.host, port=self.port)

    def connect(self):
        """
        Doesn't return, makes a blocking connection
        Only use if you are ONLY using REST
        This is a more robust REST server than get_future makes
        see:
        https://sanic.readthedocs.io/en/latest/sanic/deploying.html#asynchronous-support
        """
        return self.app.run(
            host=self.host,
            access_log=False,
            port=self.port,
            workers=self.workers,
            debug=self.debug,
        )
