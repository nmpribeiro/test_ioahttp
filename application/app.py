
from inspect import _void
from numbers import Number
from aiohttp.web import Application, run_app
from .controllers import home_controller


def create_app(pg_url) -> Application:
    app = Application()
    # app.cleanup_ctx.append(partial(init_pg, pg_url=str(pg_url)))
    app.router.add_route('GET', '/', home_controller.index)
    # app.router.add_route('POST', '/users', handle_create_user)
    return app


def main(host: str, port: Number, pg_url: str) -> _void:
    """
    Run application.
    Is called via command-line env/bin/staff-api, created by setup.py.
    """
    app = create_app(pg_url)
    run_app(app, host=host, port=port)
