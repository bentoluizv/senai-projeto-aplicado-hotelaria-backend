from ulid import ULID

from app.database.models import UserDB


def test_db_engine(engine):
    assert engine.driver == 'pysqlite'
    assert engine.name == 'sqlite'


def test_db_session(session):
    assert session.is_active
    db_user = UserDB(
        str(ULID()),
        email='bentoluizv@gmail.com',
        password='anreoa23',
        role='admin',
    )
    session.add(db_user)
    assert session.is_modified
    session.commit()
    user = session.get_one(UserDB, db_user.ulid)
    assert user is db_user
