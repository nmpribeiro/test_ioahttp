from aiohttp import web


def index(request: web.Request) -> web.Response:
    return web.Response(text="Hello world")
