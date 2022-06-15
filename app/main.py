
from inspect import _void
from numbers import Number
from aiohttp.web import Application, run_app

from app import database
from app import router


def create_app(pg_url) -> Application:
    app = Application()
    database.setup(app, pg_url)
    router.setup(app)
    return app


def run(host: str, port: Number, pg_url: str) -> _void:
    """
    Run application.
    """
    app = create_app(pg_url)
    run_app(app, host=host, port=port)
