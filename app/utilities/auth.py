from dataclasses import dataclass
import json
import random
import string
from typing import Optional
from aiohttp import web
import aiohttp
from aiohttp_session import get_session
from app.settings.conf import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, HOST, PORT


@dataclass
class SessionKeyData:
    USER_KEY: str
    STATE_KEY: str


SESSION = SessionKeyData('user', 'auth0_state')


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


async def authenticate(code: string):
    async with aiohttp.ClientSession() as client:
        async with client.post(f"https://{AUTH0_DOMAIN}/oauth/token", json={
            "grant_type": "authorization_code",
            "client_id": f"{AUTH0_CLIENT_ID}",
            "client_secret": f"{AUTH0_CLIENT_SECRET}",
            "code": f"{code}",
            "redirect_uri": f"{get_redirect_url()}"
        }) as resp:
            payload = await resp.read()
            json_res = json.loads(
                payload.decode("utf-8").replace("'", '"'))

            async with aiohttp.ClientSession() as client2:
                headers = {
                    "Authorization": f"{json_res['token_type']} {json_res['access_token']}"
                }
                async with client2.get(f"https://{AUTH0_DOMAIN}/userinfo", headers=headers) as resp:
                    payload = await resp.read()
                    user = json.loads(
                        payload.decode("utf-8").replace("'", '"'))
                    return user


async def reset_session(request: web.Request):
    session = await get_session(request)
    session[SESSION.STATE_KEY] = None
    session[SESSION.USER_KEY] = None


async def is_auth(request: web.Request):
    session = await get_session(request)
    return session[SESSION.USER_KEY] != None


async def get_user(request: web.Request):
    session = await get_session(request)
    return session[SESSION.USER_KEY]
