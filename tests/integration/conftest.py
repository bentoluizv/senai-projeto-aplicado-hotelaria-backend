from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from ulid import ULID

from app.app import app
from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.database.db import get_database_session
from app.infra.database.models import (
    AccommodationDB,
    AmenitieDB,
    Base,
    BookingDB,
    GuestDB,
    UserDB,
)
from app.schemas.User import Role


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
        new_user = UserDB(
            ulid=str(ULID.from_str('01J9V6358SNSQKF3K2GM6N4G6F')),
            email='teste@teste.com',
            password='superhardpassword',
            role=Role.ADMIN,
        )

        new_guest = GuestDB(
            ulid='01J9V645ZGN1JMCEFT9WVKQGBC',
            document='1233454345',
            name='Bento',
            surname='Machado',
            country='Brasil',
            phone='4874523452',
        )

        new_amenities = [AmenitieDB(name='wifi'), AmenitieDB(name='ducha')]

        new_accommodation = AccommodationDB(
            ulid='01J9V65AWQ1ME0J2SCYBD5S8B1',
            double_beds=2,
            name='Quarto de Teste',
            price=250,
            single_beds=0,
            status='Disponível',
            total_guests=2,
            amenities=[],
        )

        new_booking = BookingDB(
            ulid='01J9V65YSN6Z27MZ3AFSB14G6N',
            budget=8000,
            check_in=datetime(2024, 12, 22),
            check_out=datetime(2025, 1, 7),
            accommodation=new_accommodation,
            guest=new_guest,
        )

        session.add(new_guest)
        session.add(new_user)
        session.add_all(new_amenities)
        session.add(new_accommodation)
        session.add(new_booking)

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
    return RepositoryFactory(session)
