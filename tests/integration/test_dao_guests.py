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
        'document': "03093331056",
        'created_at': datetime.now().isoformat(),
        'name': 'Ana Claudia',
        'surname': 'Costa',
        'country': 'Brazil',
        'phones': ['4832395853']
    }

    guest_dao.insert(data)
    assert guest_dao.count()[0] == 5


def test_select(guest_dao):
    res = guest_dao.select({ 'document': "00157624242" })
    assert res['name'] == 'Bento Luiz'


def test_select_many(guest_dao):
    res = guest_dao.select_many()
    assert len(res) == 4

def test_update(guest_dao):
    data_to_update = {
        'document': "00157624242",
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phones': ['4832395853']
    }

    guest_dao.update(data_to_update)
    res = guest_dao.select({'document': data_to_update['document']})
    assert res['surname'] == 'V M da S Neto'


def test_delete(guest_dao):
    guest_dao.delete({ 'document': "00157624242" })
    res = guest_dao.select({ 'document': "00157624242" })
    assert res is None