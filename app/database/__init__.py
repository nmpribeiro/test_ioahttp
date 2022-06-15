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
    try:
        await app['pg'].init(PG_URL)
        try:
            yield
        finally:
            await app['pg'].pool.close()
    except Exception as err:
        print(f"Oops! Database not initiated {err=}, {type(err)=}")


def setup(app: web.Application) -> _void:
    app.cleanup_ctx.append(partial(init_pg))
