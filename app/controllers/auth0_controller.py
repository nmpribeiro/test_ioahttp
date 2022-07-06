from aiohttp import web
from aiohttp_session import get_session
from app.settings.conf import AUTH0_CLIENT_ID, AUTH0_DOMAIN, AUTH0_SCOPE
from app.utilities.auth import SESSION, get_random_string, get_redirect_url, authenticate, get_is_auth, reset_session


routes = web.RouteTableDef()


@routes.get('/auth/login')
async def handler(request: web.Request) -> web.Response:
    # return web.Response(text="Will login")
    session = await get_session(request)
    state = get_random_string(16)
    session[SESSION.STATE_KEY] = state
    raise web.HTTPFound(
        # &audience={AUTH0_AUDIENCE}
        f"https://{AUTH0_DOMAIN}/authorize?response_type=code&scope={AUTH0_SCOPE}&client_id={AUTH0_CLIENT_ID}&state={state}&redirect_uri={get_redirect_url()}"
    )


@routes.get('/auth/callback')
async def handler(request: web.Request) -> web.Response:
    # get code and state
    code_param = request.rel_url.query['code']
    state_param = request.rel_url.query['state']

    session = await get_session(request)
    state = session[SESSION.STATE_KEY]
    if (state == state_param):
        tokens = await authenticate(code_param)
        session[SESSION.TOKENS_KEY] = tokens
        raise web.HTTPFound("/")
    else:
        raise web.HTTPBadRequest()


@routes.get('/auth/logout')
async def handler(request: web.Request) -> web.Response:
    (is_auth, user) = await get_is_auth(request)
    if is_auth:
        print("Is auth, logging out")
        await reset_session(request)
        raise web.HTTPFound("/")
    else:
        print("Not auth, no need to logout")
        raise web.HTTPFound("/")
