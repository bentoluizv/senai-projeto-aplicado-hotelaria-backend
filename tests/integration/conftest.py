import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.app import app
from app.database.db import get_database_session
from app.database.models import (
    AccommodationDB,
    Base,
    GuestDB,
    UserDB,
)
from app.entities.User import User, UserCreateDTO
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
def db_user(session):
    dto = UserCreateDTO(
        email='bentoluizv@gmail.com',
        password='12334',
        password2='12334',
        role='admin',
    )
    user = User.create(dto)
    db_user = UserDB(
        email=user.email,
        password=user.password,
        role=user.role.value,
    )

    db_user.ulid = '01JAKF4V6FMQ7BEB62XVCA9KZH'
    session.add(db_user)
    session.commit()
    return db_user


@pytest.fixture()
def db_guest(session):
    guest = GuestDB(
        document='82634274',
        name='Carlos',
        surname='Anderson',
        country='Brasil',
        phone='389201221',
    )

    db_guest.ulid = '01JDHPW6E1C2Z60AWCJPP6RMN5'
    session.add(guest)
    session.commit()
    return guest


@pytest.fixture()
def db_accommodation(session):
    db_accommodation = AccommodationDB(
        name='Downhill Tent',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=50.0,
        status='disponivel',
    )

    db_accommodation.ulid = '01JDHQ1VBNGENRRWSB13J9C9TK'
    session.add(db_accommodation)
    session.commit()
    return db_accommodation
