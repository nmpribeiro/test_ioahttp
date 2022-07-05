import asyncio
import aioredis
import aiohttp_session
from aiohttp_session.redis_storage import RedisStorage

from app.settings.conf import REDIS


async def make_redis_pool() -> aioredis.Redis:
    return await aioredis.from_url(REDIS)


def session_middleware() -> aiohttp_session.Middleware:
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    storage = RedisStorage(
        redis_pool=redis_pool,
        cookie_name="AIOHTTP_SESSION",
        domain=None,
        max_age=None,
        path='/',
        secure=None,
        httponly=True
    )
    return aiohttp_session.session_middleware(storage)
