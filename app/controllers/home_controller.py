from aiohttp import web
from app.utilities import html_response

from app.utilities.auth import get_user, is_auth


routes = web.RouteTableDef()


@routes.get('/')
async def handler(request: web.Request) -> web.Response:
    # return web.Response(text="Hello world")
    if await is_auth(request):
        user = await get_user(request)
        text = f"Hello world, <br />user: {user['email']} <br /> <a href='/auth/logout'>logout</>"
    else:
        text = "Hello world, <br />user: NO USER <br /> <a href='/auth/login'>login</>"
    return html_response(text)


# @routes.get('/{username}')
# async def greet_user(request: web.Request) -> web.Response:
#     user = request.match_info.get("username", "")
#     page_num = request.rel_url.query.get("page", "")
#     return web.Response(text=f"Hello, {user} {page_num}")


@routes.post('/add_user')
async def add_user(request: web.Request) -> web.Response:
    data = await request.post()
    username = data.get('username')
    # Add the user
    # ...
    return web.Response(text=f"{username} was added")


@routes.get('/json')
async def handler(request):
    args = await request.json()
    data = {'value': args['key']}
    return web.json_response(data)
