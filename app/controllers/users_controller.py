from http import HTTPStatus

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import json_response
from asyncpg import NotNullViolationError

from models.users import users_table

routes = web.RouteTableDef()


@routes.post('/users')
async def handle_create_user(request):
    """
    Handler, creates new user
    """
    data = await request.json()

    try:
        query = users_table.insert().values(
            email=data['email'],
            name=data.get('name'),
            gender=data.get('gender'),
            floor=data.get('floor'),
            seat=data.get('seat')
        ).returning(users_table)
        row = await request.app['pg'].fetchrow(query)
        return json_response(dict(row), status=HTTPStatus.CREATED)
    except NotNullViolationError:
        raise HTTPBadRequest()
