import pytest

from app.data.dao.GuestDAO import GuestDAO
from app.data.dao.schemas.GuestSchema import GuestCreationalSchema
from app.data.database.sqlite.db import get_db


@pytest.fixture()
def guest_dao(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        yield dao


def test_guest_dao_count(guest_dao):
    TOTAL_GUESTS = 4

    assert guest_dao.count() == TOTAL_GUESTS


def test_guest_dao_find_many(guest_dao):
    TOTAL_GUESTS = 4
    guests = guest_dao.find_many()
    assert len(guests) == TOTAL_GUESTS


def test_guest_dao_find(guest_dao):
    guest = guest_dao.find('00157624242')
    assert guest


def test_guest_dao_find_by(guest_dao):
    guest = guest_dao.find_by('name', 'Bento')
    assert guest


def test_guest_dao_create(guest_dao):
    TOTAL_GUESTS = 5

    data = GuestCreationalSchema(**{
        'document': '03093331056',
        'name': 'Ana',
        'surname': 'Costa',
        'country': 'Brazil',
        'phone': '48xxxxxxxx',
    })
    guest_dao.create(data)

    assert guest_dao.count() == TOTAL_GUESTS


def test_guest_dao_update(guest_dao):
    exists = guest_dao.find_by('document', '00157624242')
    assert exists is not None

    data = {
        'document': '00157624242',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': ' 4832395853',
    }

    guest_dao.update(GuestCreationalSchema(**data))
    guest = guest_dao.find('00157624242')
    assert guest.surname == 'V M da S Neto'


def test_guest_dao_delete(guest_dao):
    guest_dao.delete('00157624242')
    res = guest_dao.find('00157624242')
    assert not res
