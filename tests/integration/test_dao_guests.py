from pytest import fixture
import pytest
from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.entity.Guests import Guest, GuestDTO

@fixture
def guest_dao(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        yield dao

def test_guest_dao_count(guest_dao):
    assert guest_dao.count() == 4

def test_guest_dao_insert(guest_dao):
    guest_dto: GuestDTO = {
        'document':'03093331056',
        'name':'Ana Claudia',
        'surname':'Costa',
        'country':'Brazil',
        'phone':'4832395853',
        'created_at': '2024-05-22T10:56:45.439704'
        }
    guest_dao.insert(guest_dto)
    assert guest_dao.count() == 5


def test_guest_dao_select(guest_dao):
    guest = guest_dao.find("00157624242")
    assert guest['name'] == 'Bento Luiz'


def test_guest_dao_select_many(guest_dao):
    res = guest_dao.find_many()
    assert len(res) == 4


def test_guest_dao_update(guest_dao):
    exists = guest_dao.find('00157624242')
    assert exists is not None

    guest_dto: GuestDTO = {
        'document': "00157624242",
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone':' 4832395853',
        'created_at': exists['created_at']
    }

    guest_dao.update(guest_dto)
    result = guest_dao.find("00157624242")
    assert result['surname'] == 'V M da S Neto'


def test_guest_dao_delete(guest_dao):
    guest_dao.delete("00157624242")
    res = guest_dao.find("00157624242")
    assert res is None