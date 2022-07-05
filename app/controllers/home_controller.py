from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/')
async def handler(request: web.Request) -> web.Response:
    return web.Response(text="Hello world")


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
