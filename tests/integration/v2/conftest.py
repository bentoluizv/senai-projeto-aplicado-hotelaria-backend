import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.main import app
from app.database.sqlalchemy.db_init import db_init
from app.database.sqlalchemy.models import Base


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        db_init(session)
        yield session

    Base.metadata.drop_all(engine)
