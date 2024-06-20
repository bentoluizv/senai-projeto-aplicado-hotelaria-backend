import pytest

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.sqlite.db import get_db
from app.schemas.GuestSchema import GuestSchema


@pytest.fixture()
def guest_dao(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        yield dao


def test_guest_dao_count(guest_dao):
    TOTAL_BOOKINGS = 4

    assert guest_dao.count() == TOTAL_BOOKINGS


def test_guest_dao_insert(guest_dao):
    TOTAL_BOOKINGS = 5

    data = GuestSchema(**{
        'document': '03093331056',
        'name': 'Ana',
        'surname': 'Costa',
        'country': 'Brazil',
        'phone': '48xxxxxxxx',
    })
    guest_dao.insert(data)
    assert guest_dao.count() == TOTAL_BOOKINGS


def test_guest_dao_select(guest_dao):
    guest = guest_dao.findBy('document', '00157624242')
    assert guest.name == 'Bento'


def test_guest_dao_select_many(guest_dao):
    TOTAL_BOOKINGS = 4
    guests = guest_dao.find_many()
    assert len(guests) == TOTAL_BOOKINGS


def test_guest_dao_update(guest_dao):
    exists = guest_dao.findBy('document', '00157624242')
    assert exists is not None

    data = {
        'document': '00157624242',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': ' 4832395853',
    }

    guest_dao.update(GuestSchema(**data))
    guest = guest_dao.findBy('document', '00157624242')
    assert guest.surname == 'V M da S Neto'


@pytest.mark.skip()
def test_guest_dao_delete(guest_dao):
    guest_dao.delete('00157624242')
    res = guest_dao.findBy('document', '00157624242')
    assert res is None
