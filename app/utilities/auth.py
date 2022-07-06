from dataclasses import dataclass
import json
import random
import string
from typing import Any, Dict, Optional, Tuple, Union
from aiohttp import web
import aiohttp
from aiohttp_session import Session, get_session
from app.settings.conf import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, HOST, PORT


@dataclass
class SessionKeyData:
    TOKENS_KEY: str
    STATE_KEY: str


SESSION = SessionKeyData('auth0_tokens', 'auth0_state')


# https://auth0.com/docs/secure/attack-protection/state-parameters


# https://auth0.com/docs/secure/attack-protection/state-parameters
# https://auth0.com/docs/get-started/authentication-and-authorization-flow/mitigate-replay-attacks-when-using-the-implicit-flow
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def get_redirect_url():
    host = HOST.replace("0.0.0.0", "localhost")
    return f"http://{host}:{PORT}/auth/callback"


async def authenticate(code: string) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.post(f"https://{AUTH0_DOMAIN}/oauth/token", json={
            "grant_type": "authorization_code",
            "client_id": f"{AUTH0_CLIENT_ID}",
            "client_secret": f"{AUTH0_CLIENT_SECRET}",
            "code": f"{code}",
            "redirect_uri": f"{get_redirect_url()}"
        }) as resp:
            payload = await resp.read()
            token_object = json.loads(
                payload.decode("utf-8").replace("'", '"'))
    return token_object


async def reset_session(request: web.Request):
    session = await get_session(request)
    session[SESSION.STATE_KEY] = None
    session[SESSION.TOKENS_KEY] = None


async def get_user(request: web.Request):
    session = await get_session(request)
    tokens = get_tokens(session)
    try:
        if tokens == None:
            raise Exception("no tokens")
        async with aiohttp.ClientSession() as client2:
            headers = {
                "Authorization": f"{tokens['token_type']} {tokens['access_token']}"
            }
            async with client2.get(f"https://{AUTH0_DOMAIN}/userinfo", headers=headers) as resp:
                payload = await resp.read()
                user = json.loads(
                    payload.decode("utf-8").replace("'", '"'))
                if "sub" in user:
                    return user
                else:
                    raise Exception("no user or user.sub attribute")
    except:
        await reset_session(request)
        return None


def get_tokens(session: Session) -> Dict[str, Any]:
    try:
        return session[SESSION.TOKENS_KEY]
    except:
        return None


async def get_is_auth(request: web.Request) -> Tuple[bool, Dict[str, Any]]:
    user = await get_user(request)
    is_auth = False
    if (user != None):
        is_auth = True

    return (is_auth, user)
