from inspect import _void
from aiohttp.web import Application, run_app

from app import database
from app import router
from app.middlewares import session
from app.settings.conf import HOST, PORT


def create_app() -> Application:
    try:
        database.setup()
        app = Application(middlewares=[session.session_middleware()])
        router.setup(app)
        return app
    except Exception as err:
        print(f"Oops! Application not initiated {err=}, {type(err)=}")


def run() -> _void:
    """
    Run application.
    """

    app = create_app()
    try:
        run_app(app, host=HOST, port=PORT)
    except Exception as err:
        print(f"Oops! Application run failure:\n {err=}, {type(err)=}")
