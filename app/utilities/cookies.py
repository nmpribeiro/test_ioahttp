import json
import time
from typing import Optional
import uuid
import aiohttp
from aiohttp_session import get_session

from app.models import User


def getKey(key: str):
    return 'AIOHTTP_SESSION_' + key

# https://www.gitdetail.com/repositories/adamchainz/aiohttp_session/100049
# https://www.programcreek.com/python/?code=aio-libs%2Faiohttp-session%2Faiohttp-session-master%2Ftests%2Ftest_redis_storage.py


async def make_cookie(client: aiohttp.web.Application, redis, data):
    session_data = {
        'session': data,
        'created': int(time.time())
    }
    value = json.dumps(session_data)
    key = uuid.uuid4().hex
    with await redis as conn:
        await conn.set(getKey(key), value)
    client.session.cookie_jar.update_cookies({'AIOHTTP_SESSION': key})


async def load_cookie(client: aiohttp.web.Application, redis):
    cookies = client.session.cookie_jar.filter_cookies(client.make_url('/'))
    key = cookies['AIOHTTP_SESSION']
    with await redis as conn:
        encoded = await conn.get(getKey(key.value))
        s = encoded.decode('utf-8')
        value = json.loads(s)
        return value


async def get_auth_user(request: aiohttp.request) -> Optional[User]:
    app: aiohttp.web.Application = request.app
    session = await get_session(request)
    user_id = session.get('user_id')
    User.query.filter_by()
    # return user_id
    # async with app['db'].acquire() as conn:
    #     return await User.get(conn, user_id)
