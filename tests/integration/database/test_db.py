from sqlalchemy import select

from app.database.models import UserDB


def test_db_engine(engine):
    assert engine.driver == 'pysqlite'
    assert engine.name == 'sqlite'


def test_db_session(session):
    TOTAL_USERS = 4
    users = session.scalars(select(UserDB)).all()
    assert len(users) == TOTAL_USERS
