from datetime import datetime

from pytest import fixture
from app.data.dao.guest_dao import GuestDAO
from app.data.database.db import get_db
from app.domain.Guests import Guest

@fixture
def guest_dao(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        yield dao

def test_guest_dao_count(guest_dao):
    assert guest_dao.count() == 4


def test_guest_dao_insert(guest_dao):
    guest = Guest('03093331056','Ana Claudia', 'Costa', 'Brazil', '4832395853')
    guest_dao.insert(guest)
    assert guest_dao.count() == 5


def test_guest_dao_select(guest_dao):
    guest = guest_dao.select("00157624242")
    assert guest.name == 'Bento Luiz'


def test_guest_dao_select_many(guest_dao):
    res = guest_dao.select_many()
    assert len(res) == 4

def test_guest_dao_update(guest_dao):
    exists = guest_dao.select('00157624242')
    assert exists is not None
    guest = Guest("00157624242", 'Bento Luiz', 'V M da S Neto', 'Brazil', '4832395853', exists.created_at)
    guest_dao.update(guest)
    assert guest_dao.select('00157624242').surname == 'V M da S Neto'


def test_guest_dao_delete(guest_dao):
    guest_dao.delete("00157624242")
    res = guest_dao.select("00157624242")
    assert res is None