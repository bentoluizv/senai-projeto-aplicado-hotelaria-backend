import os
import tempfile

from app import create_app
from app.data.database.db import init_db, seed_db
from pytest import fixture


@fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.app_context():
        init_db()
        seed_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@fixture
def client(app):
    return app.test_client()


@fixture
def runner(app):
    return app.test_cli_runner()
