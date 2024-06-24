import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.api.main import app
from app.database.sqlalchemy.models import GuestDB, table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    table_registry.metadata.create_all(engine)  # type: ignore

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


def test_create_guest(session):
    new_guest = GuestDB(
        document='00157624242',
        name='Bento Luiz',
        surname='Machado',
        country='Brasil',
        phone='48992054211',
    )
    session.add(new_guest)
    session.commit()

    guest = session.scalar(select(GuestDB).where(GuestDB.name == 'Bento Luiz'))

    assert guest.name == 'Bento Luiz'
