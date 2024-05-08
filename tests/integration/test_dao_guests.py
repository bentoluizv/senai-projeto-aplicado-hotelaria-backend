from datetime import datetime
from uuid import uuid4

from pytest import fixture
from app.data.dao.guest_dao import GuestDAO
from app.data.database.db import get_db

@fixture
def guest_dao(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        yield dao

def test_count(guest_dao):
    assert guest_dao.count()[0] == 4


def test_insert(guest_dao):
    data = {
        'uuid': str(uuid4()),
        'created_at': datetime.now().isoformat(),
        'name': 'Ana Claudia',
        'surname': 'Costa',
        'country': 'Brazil',
        'phones': ['4832395853']
    }

    guest_dao.insert(data)
    assert guest_dao.count()[0] == 5


def test_select(guest_dao):
    res = guest_dao.select({ 'uuid': "ed59e12f-b8e9-46ba-86ac-5ef69ea011a3" })
    assert res['name'] == 'Bento Luiz'


def test_select_many(guest_dao):
    res = guest_dao.select_many()
    assert len(res) == 4

def test_update(guest_dao):
    data_to_update = {
        'uuid': "ed59e12f-b8e9-46ba-86ac-5ef69ea011a3",
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phones': ['4832395853']
    }

    guest_dao.update(data_to_update)
    res = guest_dao.select({'uuid': data_to_update['uuid']})
    assert res['surname'] == 'V M da S Neto'


def test_delete(guest_dao):
    guest_dao.delete({ 'uuid': "ed59e12f-b8e9-46ba-86ac-5ef69ea011a3" })
    res = guest_dao.select({ 'uuid': "ed59e12f-b8e9-46ba-86ac-5ef69ea011a3" })
    assert res is None