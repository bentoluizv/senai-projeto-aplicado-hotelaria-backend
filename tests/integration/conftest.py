import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.app import app
from app.database.db import get_database_session
from app.database.models import (
    AccommodationDB,
    Base,
    BookingDB,
    GuestDB,
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


@pytest.fixture()
def db_booking(session):
    query = select(BookingDB)
    db_booking = session.scalars(query).first()
    db_booking.ulid = '01JA5EZ0BBQRGDX69PNTVG3N5E'
    session.commit()
    return db_booking


@pytest.fixture()
def db_guest(session):
    query = select(GuestDB)
    db_guest = session.scalars(query).first()
    db_guest.ulid = '01JA5EZ0BBQRGDX69PNTVG3N5E'
    db_guest.document = '2672713987'
    session.commit()
    return db_guest


@pytest.fixture()
def db_accommodation(session):
    query = select(AccommodationDB)
    db_accommodation = session.scalars(query).first()
    db_accommodation.ulid = '01JA5EZ0BBQRGDX69PNTVG3N5E'
    session.commit()
    return db_accommodation
