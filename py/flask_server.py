from typing import Callable
from typing import Any


from time import sleep
from functools import wraps

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import CancelledError
from concurrent.futures import wait

from werkzeug.exceptions import BadRequest

import flask
from flask import Flask
from flask import jsonify
from flask import request as flask_request
from flask import Response

from utils import APIArgs, APIResponse

task_threadpool = ThreadPoolExecutor(
    max_workers=None,
    thread_name_prefix="pool",
    initializer=None,
    initargs=())

TIMEOUT = 5

Func = Callable[..., Any]
APIFunc = Callable[[APIArgs, APIResponse], None]
WrappedAPIFunc = Callable[[], Response]


def _get_args(request: flask.Request) -> APIArgs:  # {{{
    """Get the parameters from the HTTP request.

    Args:
        request: The HTTP request to get the parameters from.

    Returns:
        The populated `APIArgs` struct.
    """
    try:
        args = request.get_json()
        text: str = args.get("text", "")
        count: int = int(args.get("count", -1))

        if count <= 0:
            raise ValueError("Invalid count requested")

    except ValueError as err:
        raise BadRequest(description=str(err)) from err

    return APIArgs(text, count)
# }}}


def rewrite_entrypoint(f: APIFunc) -> WrappedAPIFunc:  # {{{
    """Decorate a Flask endpoint to add parameter parsing."""
    @wraps(f)
    def wrap(**kwargs) -> Response:
        api_args: APIArgs = _get_args(flask_request)
        resp = APIResponse([])
        try:
            f(api_args, resp, **kwargs)
        except Exception as err:
            return Response(f"Server encountered an unknown error: {err}", 500)
        return jsonify(resp)
    return wrap  # }}}


def task(sleep_time: float, text: str) -> str:
    sleep(sleep_time)
    return text


@rewrite_entrypoint
def entry(args: APIArgs,
          resp: APIResponse,
          ) -> None:
    futures = {}

    for sleep_time in [0.5, 1, 2] * args.count:
        fut = task_threadpool.submit(task, sleep_time, args.text)
        futures[fut] = (sleep_time)

    done, not_done = wait(futures.keys(), timeout=TIMEOUT)

    for future in done:
        try:
            resp.texts.append(future.result())
        except CancelledError:
            pass

    for future in not_done:
        future.cancel()


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)
    app.add_url_rule("/", view_func=entry, methods=["GET", "POST"])
    return app
