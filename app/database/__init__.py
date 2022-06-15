from functools import partial

from aiohttp import web
from asyncpgsa import PG
from inspect import _void
from app.settings.conf import PG_URL


async def init_pg(app):
    """
    Init asyncpgsa driver (asyncpg + sqlalchemy)
    """
    app['pg'] = PG()
    await app['pg'].init(PG_URL)
    try:
        yield
    finally:
        await app['pg'].pool.close()


def setup(app: web.Application) -> _void:
    app.cleanup_ctx.append(partial(init_pg))
