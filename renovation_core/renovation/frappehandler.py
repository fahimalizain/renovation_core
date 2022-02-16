# from contextvars import ContextVar, Token
import os
import typing

import anyio
from fastapi import Request, Response
from starlette.responses import StreamingResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.middleware.wsgi import WSGIResponder
from asyncer import asyncify

import frappe
import frappe.app
import frappe.auth
from werkzeug.middleware.shared_data import SharedDataMiddleware
from frappe.middlewares import StaticDataMiddleware

from renovation.utils.async_db import thread_safe_db, obtain_pool_connection

frappe.app._site = os.environ.get("SITE_NAME", "test.localhost")
frappe_application = SharedDataMiddleware(frappe.app.application, {
    str('/assets'): str(os.path.join(frappe.app._sites_path, 'assets'))
})

frappe_application = StaticDataMiddleware(frappe_application, {
    str('/files'): str(os.path.abspath(frappe.app._sites_path))
})


def _connect(site=None, db_name=None, set_admin_as_user=True):
    """Connect to site database instance.

    :param site: If site is given, calls `frappe.init`.
    :param db_name: Optional. Will use from `site_config.json`.
    :param set_admin_as_user: Set Administrator as current user.
    """
    from frappe.database import get_db
    if site:
        frappe.init(site)

    frappe.local.db = get_db(user=db_name or frappe.local.conf.db_name)
    obtain_pool_connection(frappe.local.db)
    thread_safe_db(frappe.local.db)
    if set_admin_as_user:
        frappe.set_user("Administrator")

# The following two overrides exists
# Since we use frappe.app.init_request (which invokes TWO DB Connections o.O FRAPPE BUG)
frappe.auth.HTTPRequest.connect = lambda *args, **kwargs: None
frappe.connect = _connect

class FrappeMiddleware:
    # Copy of starlette.middleware.BaseHTTPMiddleware
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def call_next(request: Request) -> Response:
            app_exc: typing.Optional[Exception] = None
            send_stream, recv_stream = anyio.create_memory_object_stream()

            async def coro() -> None:
                nonlocal app_exc

                async with send_stream:
                    try:
                        await self.app(scope, request.receive, send_stream.send)
                    except Exception as exc:
                        app_exc = exc

            task_group.start_soon(coro)

            try:
                message = await recv_stream.receive()
            except anyio.EndOfStream:
                if app_exc is not None:
                    raise app_exc
                raise RuntimeError("No response returned.")

            assert message["type"] == "http.response.start"

            async def body_stream() -> typing.AsyncGenerator[bytes, None]:
                async with recv_stream:
                    async for message in recv_stream:
                        assert message["type"] == "http.response.body"
                        yield message.get("body", b"")

                if app_exc is not None:
                    raise app_exc

            response = StreamingResponse(
                status_code=message["status"], content=body_stream()
            )
            response.raw_headers = message["headers"]
            return response

        async with anyio.create_task_group() as task_group:
            request = Request(scope, receive=receive)
            response = await self.dispatch_func(request, call_next, scope, receive, send)
            if response and callable(response):
                await response(scope, receive, send)
            task_group.cancel_scope.cancel()

    async def dispatch_func(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
            scope: Scope,
            receive: Receive,
            send: Send) -> Response:

        response = None
        try:
            await make_wsgi_compatible(request=request)
            frappe.app.init_request(request=request)

            response = await call_next(request)

            if response and response.status_code == 404 and frappe.conf.get("developer_mode"):
                frappe.destroy()  # Let frappe init fresh
                responder = WSGIResponder(frappe_application, scope)

                # receive is basically reading request-body
                message = {
                    "type": "http.request",
                    "body": request._body,
                    "more_body": False,
                }
                await responder(asyncify(lambda: message), send)
                response = None

        except BaseException as e:
            print(frappe.get_traceback())
            response = Response()
            response.status_code = 500
            response.body = frappe.safe_encode(frappe.as_json(dict(
                title=str(e),
                traceback=frappe.get_traceback()
            )))
        finally:
            frappe.destroy()

        return response


async def make_wsgi_compatible(request: Request):
    request.environ = None
    request.host = request.client.host
    request.path = request.url.path
    request.scheme = request.url.scheme
    request.content_type = request.headers.get("content-type", None)

    request.accept_languages = request.headers.get("accept-language", None)
    if request.accept_languages:  # 'en-US,en;q=0.9'
        _lang = dict()
        for i, lang in enumerate(request.accept_languages.split(";")[0].split(",")):
            _lang[i] = lang
        request.accept_languages = _lang
    else:
        request.accept_languages = dict()

    # !important to ask for body before form
    body = frappe.safe_decode(await request.body())
    # python-multipart==0.0.5 dependency
    form = await request.form()
    request.form = form

    request.args = request.query_params
    request.get_data = lambda **kwargs: body