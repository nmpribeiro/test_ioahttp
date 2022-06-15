from functools import partial

from aiohttp import web
from asyncpgsa import PG

from inspect import _void
# from typing import AsyncIterator
# import aiosqlite


async def init_pg(app, pg_url):
    """
    Init asyncpgsa driver (asyncpg + sqlalchemy)
    """
    app['pg'] = PG()
    await app['pg'].init(pg_url)
    try:
        yield
    finally:
        await app['pg'].pool.close()


# async def init_sqlite(app: web.Application) -> AsyncIterator[None]:
#     db = await aiosqlite.connect("db.sqlite")
#     app["DB"] = db
#     yield
#     await db.close()


def setup(app: web.Application,  pg_url: str) -> _void:
    app.cleanup_ctx.append(partial(init_pg, pg_url=str(pg_url)))
    # app.cleanup_ctx.append(init_sqlite)
