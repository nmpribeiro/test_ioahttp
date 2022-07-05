from abc import abstractmethod
from app.database import get_session
from sqlalchemy import inspect, select, update as sqlalchemy_update
import sqlalchemy as sa
from sqlalchemy.orm import configure_mappers, declarative_base


Base = declarative_base()


# Taken from https://ahmed-nafies.medium.com/sqlalchemy-async-orm-is-finally-here-d560dfaa335d

class BaseModel():
    @abstractmethod
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        with get_session().begin() as session:
            session.add(cls(**kwargs))

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        with get_session().begin() as session:
            session.execute(query)

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        with get_session().begin() as session:
            results = session.execute(query)
            (result,) = results.one()
        return result

    @classmethod
    async def all(cls: BaseModel):
        with get_session().begin() as session:
            result = session.query(cls).all()
            arr = []
            for item in result:
                arr.append(item.toDict())
        return arr


class User(Base, BaseModel, ModelAdmin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    user_id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(256), nullable=False, unique=True)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, user_id={self.user_id!r})"


configure_mappers()
