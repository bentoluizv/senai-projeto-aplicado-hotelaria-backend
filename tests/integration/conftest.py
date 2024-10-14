import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.app import app
from app.database.db import get_database_session
from app.database.models import (
    Base,
    BookingDB,
)
from app.factory.RepositoryFactory import RepositoryFactory
from app.utils.populate_db import populate_db


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        'sqlite+pysqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    return engine


@pytest.fixture()
def session(engine):
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        populate_db(session)
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_database_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def repository_factory(session):
    return RepositoryFactory(session=session)


@pytest.fixture(autouse=True)
def _db_booking(session):
    query = select(BookingDB)
    db_booking = session.scalars(query).first()
    db_booking.ulid = '01JA5EZ0BBQRGDX69PNTVG3N5E'
    session.commit()
