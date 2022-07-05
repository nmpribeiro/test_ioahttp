from aiohttp import web

from app.utilities.cookies import get_auth_user


routes = web.RouteTableDef()


@routes.get('/auth/login')
async def handler(request: web.Request) -> web.Response:
    return web.Response(text="Will login")


@routes.get('/auth/callback')
async def handler(request: web.Request) -> web.Response:
    return web.Response(text="Will callback")


@routes.get('/auth/logout')
async def handler(request: web.Request) -> web.Response:
    app: web.Application = request.app
    auth_user = await get_auth_user(request)
    return web.Response(text="Will logout")
