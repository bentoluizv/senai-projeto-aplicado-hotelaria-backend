from datetime import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.app import app
from app.data.database.models import (
    AccommodationDB,
    AmenitieDB,
    Base,
    BookingDB,
    GuestDB,
    UserDB,
)


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
            uuid=UUID('6ab53765-3a8f-40a1-89e6-0b9834187f22'),
            email='teste@teste.com',
            password='superhardpassword',
        )

        new_guest = GuestDB(
            document='00157624242',
            name='Bento',
            surname='Machado',
            country='Brasil',
            phone='48992054211',
        )

        new_amenities = [AmenitieDB(name='wifi'), AmenitieDB(name='ducha')]

        new_accommodation = AccommodationDB(
            double_beds=2,
            name='Quarto de Teste',
            price=250,
            single_beds=0,
            status='Disponível',
            total_guests=2,
            amenities=[],
        )

        new_booking = BookingDB(
            budget=8000,
            check_in=datetime(2024, 12, 22),
            check_out=datetime(2025, 1, 7),
            status='Aguardando Check In',
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
def client():
    with TestClient(app) as client:
        yield client
