from inspect import _void
from aiohttp import web

from app.controllers import home_controller


def setup(app: web.Application) -> _void:
    # Add your controllers here
    app.add_routes(home_controller.routes)
