from dataclasses import dataclass
import json
import random
import string
from typing import Any, Dict, Tuple
from aiohttp import ClientResponse, web
import aiohttp
from aiohttp_session import Session, get_session
from app.settings.conf import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, AUTH0_SCOPE, AUTH0_AUDIENCE, HOST, PORT
from app.utilities.utils import byte_to_json, print_json


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


async def get_data_from_resp(resp: ClientResponse):
    payload = await resp.read()
    if resp.status != 200:
        # if payload == ""
        json = byte_to_json(payload, False)
        print_json(json)
        raise Exception(
            f"auth request status {resp.status} | {json.get('error_description')}")
    return byte_to_json(payload)


async def authenticate(code: string) -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as client:
            async with client.post(f"https://{AUTH0_DOMAIN}/oauth/token", json={
                "grant_type": "authorization_code",
                "scope": f"{AUTH0_SCOPE}",
                "audience": f"{AUTH0_AUDIENCE}",
                "client_id": f"{AUTH0_CLIENT_ID}",
                "code": f"{code}",
                "redirect_uri": f"{get_redirect_url()}"
            }) as resp:
                return await get_data_from_resp(resp)
    except Exception as e:
        print(f"[auth][authenticate()] error: {e}")
        return None


async def authenticate_test(email: string, password: string) -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as client:
            async with client.post(f"https://{AUTH0_DOMAIN}/oauth/token", json={
                "grant_type": "password",
                "scope": f"{AUTH0_SCOPE}",
                "audience": f"{AUTH0_AUDIENCE}",
                "client_id": f"{AUTH0_CLIENT_ID}",
                "client_secret": f"{AUTH0_CLIENT_SECRET}",
                "username": f"{email}",
                "password": f"{password}"
            }) as resp:
                return await get_data_from_resp(resp)
    except Exception as e:
        print(f"[auth][authenticate_test()] error: {e}")
        return None


async def reset_session(request: web.Request):
    session = await get_session(request)
    session[SESSION.STATE_KEY] = None
    session[SESSION.TOKENS_KEY] = None


def get_auth_header(tokens: Dict[str, Any]) -> Dict[str, str]:
    return {"Authorization": f"{tokens['token_type']} {tokens['access_token']}"}


async def get_user(request: web.Request):
    session = await get_session(request)
    tokens = get_tokens(session)
    try:
        if tokens == None:
            raise Exception("no tokens")
        async with aiohttp.ClientSession() as client:
            async with client.get(f"https://{AUTH0_DOMAIN}/userinfo", headers=get_auth_header(tokens)) as resp:
                user = await get_data_from_resp(resp)
                if "sub" in user:
                    return user

        raise Exception("no user or user.sub attr or something weird happened")
    except:
        await reset_session(request)
        return None


def get_tokens(session: Session) -> Dict[str, Any]:
    if SESSION.TOKENS_KEY in session:
        return session[SESSION.TOKENS_KEY]
    else:
        return None


async def get_is_auth(request: web.Request) -> Tuple[bool, Dict[str, Any]]:
    user = await get_user(request)
    is_auth = False
    if (user != None):
        is_auth = True

    return (is_auth, user)
