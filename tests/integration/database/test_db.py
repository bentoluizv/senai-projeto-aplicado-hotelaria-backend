from sqlalchemy import select

from app.infra.models import UserDB


def test_db_engine(engine):
    assert engine.driver == 'pysqlite'
    assert engine.name == 'sqlite'


def test_db_session(session):
    users = session.scalars(select(UserDB)).all()
    assert len(users) == 0

    user = session.scalar(
        select(UserDB).where(UserDB.email == 'teste@teste.com')
    )

    assert not user
