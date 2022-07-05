from inspect import _void
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings.conf import PG_URL

Base = declarative_base()

# https://jupyter-tutorial.readthedocs.io/de/latest/data-processing/postgresql/sqlalchemy.html


def get_engine():
    return create_engine(PG_URL, echo=True)


# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(get_engine())


def get_session():
    return Session


def setup() -> _void:
    Base.metadata.create_all(get_engine())
