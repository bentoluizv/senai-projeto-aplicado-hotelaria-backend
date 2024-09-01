import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.app import app
from app.infra.database.models import (
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
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
