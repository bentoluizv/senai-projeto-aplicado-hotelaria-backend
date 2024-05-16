import os
import tempfile

from pytest import fixture

from app import create_app
from app.data.database.db import init_db, seed_db


with open(os.path.join(os.path.dirname(__file__), '/home/bentoluiz/Workspace/senai_projeto_aplicado_01/app/data/database/seed.sql'), 'rb') as f:
    _data_sql = f.read().decode()

@fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

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