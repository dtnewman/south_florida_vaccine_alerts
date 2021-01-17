"""
Database module, including the SQLAlchemy database object and DB-related utilities.
"""
import sqlalchemy
from sqlalchemy.orm import relationship
from .extensions import db
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.ext.declarative import declarative_base


# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship

engine = None
db_session = scoped_session(lambda: create_session(autocommit=False, autoflush=False, expire_on_commit=True, bind=engine))


def init_engine(uri, **kwargs):
    global engine
    engine = sqlalchemy.create_engine(uri, **kwargs)
    return engine


def init_db():
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(bind=engine)