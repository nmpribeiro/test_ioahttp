import sqlalchemy as sa
from sqlalchemy.orm import configure_mappers, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    user_id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(256), nullable=False, unique=True)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, user_id={self.user_id!r})"


configure_mappers()
