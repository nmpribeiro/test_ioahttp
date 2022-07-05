from app.models import User
from http import HTTPStatus

from aiohttp import request, web
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import json_response
from asyncpg import NotNullViolationError
from asyncpgsa import PG

from sqlalchemy import func, select, text
from sqlalchemy.orm import sessionmaker


routes = web.RouteTableDef()


@routes.get('/users')
async def handle_get_users(request: request):
    # s.query(Book).all()
    """
    Handler, creates new user
    """
    users = await User.all()
    # s.query(Book)
    # query = select().select_from(User.__tablename__)
    # users = await pg.fetch(query)
    return json_response(users, status=HTTPStatus.OK)


@routes.post('/users')
async def handle_create_user(request):
    """
    Handler, creates new user
    """

# @routes.post('/users')
# async def handle_create_user(request):
#     """
#     Handler, creates new user
#     """
#     data = await request.json()

#     try:
#         query = users_table.insert().values(
#             email=data['email'],
#             name=data.get('name'),
#             gender=data.get('gender'),
#             floor=data.get('floor'),
#             seat=data.get('seat')
#         ).returning(users_table)
#         row = await request.app['pg'].fetchrow(query)
#         return json_response(dict(row), status=HTTPStatus.CREATED)
#     except NotNullViolationError:
#         raise HTTPBadRequest()
