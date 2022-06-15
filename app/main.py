
from inspect import _void

from aiohttp.web import Application, run_app

from app import database
from app import router
from app.settings.conf import HOST, PORT


def create_app() -> Application:
    app = Application()
    database.setup(app)
    router.setup(app)
    return app


def run() -> _void:
    """
    Run application.
    """
    app = create_app()
    run_app(app, host=HOST, port=PORT)
