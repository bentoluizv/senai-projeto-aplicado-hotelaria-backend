import datetime

import pytest

from app.database.sqlalchemy.repository.GuestRepository import GuestRepository
from app.domain.Guest import Guest
from app.errors.NotFoundError import NotFoundError


@pytest.fixture()
def guest_repository(session):
    guest_repository = GuestRepository(session)

    return guest_repository


def test_guest_repository_find_many(guest_repository):
    TOTAL_GUESTS = 5
    guests = guest_repository.find_many()
    assert len(guests) == TOTAL_GUESTS


def test_guest_repository_find(guest_repository):
    guest = guest_repository.find('123.456.789-00')
    assert guest
    assert isinstance(guest, Guest)


def test_guest_repository_find_by(guest_repository):
    guest = guest_repository.find_by_name('Maria')
    assert guest
    assert guest[0].document == '987.654.321-00'


def test_guest_repository_create(guest_repository):
    guest = Guest(
        name='Ana',
        document='030.933.310-56',
        surname='Costa',
        country='Brasil',
        phone='+55 48 98767-2435',
        created_at=datetime.datetime.now(),
    )
    guest_repository.create(guest)

    assert guest_repository.find('030.933.310-56')


def test_guest_repository_update(guest_repository):
    guest = Guest(
        document='987.654.321-00',
        created_at=datetime.datetime.now(),
        name='Maria',
        surname='Ramos',
        country='Brasil',
        phone='+55 48 93239-5853',
    )

    guest_repository.update(guest)
    guest = guest_repository.find('987.654.321-00')
    assert guest.surname == 'Ramos'


def test_guest_repository_delete(guest_repository):
    guest_repository.delete('987.654.321-00')
    with pytest.raises(NotFoundError):
        guest_repository.delete('987.654.321-00')
