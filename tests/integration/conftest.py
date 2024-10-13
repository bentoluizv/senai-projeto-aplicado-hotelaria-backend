import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.app import app
from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.db import get_database_session
from app.infra.models import (
    Base,
)
from app.infra.populate_db import populate_database
from app.services.BookingService import BookingService


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
        populate_database(session)
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


@pytest.fixture()
def booking_service(repository_factory):
    return BookingService(repository_factory)
