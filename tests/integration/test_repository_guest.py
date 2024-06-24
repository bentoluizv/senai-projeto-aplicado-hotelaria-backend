import pytest

from app.database.sqlite.dao.GuestDAO import GuestDAO
from app.database.sqlite.db import get_db
from app.database.sqlite.repository.GuestRepository import GuestRepository
from app.errors.NotFoundError import NotFoundError


@pytest.fixture()
def guest_repository(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        guest_repository = GuestRepository(dao)
        yield guest_repository


def test_guest_repository_find_many(guest_repository):
    TOTAL_BOOKINGS = 4
    guests = guest_repository.find_many()
    assert len(guests) == TOTAL_BOOKINGS


def test_guest_repository_find(guest_repository):
    guest = guest_repository.find('00157624242')
    assert guest


def test_guest_repository_find_by(guest_repository):
    guest = guest_repository.find_by('name', 'Bento')
    assert guest


def test_guest_repository_create(guest_repository):
    data = {
        'document': '03093331056',
        'name': 'Ana',
        'surname': 'Costa',
        'country': 'Brazil',
        'phone': '48xxxxxxxx',
    }
    guest_repository.create(data)

    assert guest_repository.find('03093331056')


def test_guest_repository_update(guest_repository):
    exists = guest_repository.find_by('document', '00157624242')
    assert exists is not None

    data = {
        'document': '00157624242',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': ' 4832395853',
    }

    guest_repository.update(data)
    guest = guest_repository.find('00157624242')
    assert guest.surname == 'V M da S Neto'


def test_guest_repository_delete(guest_repository):
    guest_repository.delete('00157624242')
    with pytest.raises(NotFoundError):
        guest_repository.find('00157624242')
