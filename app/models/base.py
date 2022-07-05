from sqlalchemy import select, update as sqlalchemy_update

from app.database import get_session


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        session = get_session()
        session.add(cls(**kwargs))
        session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        session = get_session()
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        session.execute(query)
        session.commit()

    @classmethod
    async def get(cls, id):
        session = get_session()
        query = select(cls).where(cls.id == id)
        results = session.execute(query)
        (result,) = results.one()
        return result

    @classmethod
    async def all(cls):
        session = get_session()
        result = session.query(cls).all()
        return result
