import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.database.models import GuestDB
from app.entities.Guest import Guest, GuestCreateDTO, GuestUpdateDTO


@pytest.fixture()
def guest_repository(repository_factory):
    guest_repository = repository_factory.create_guest_respository()
    return guest_repository


def test_list_all_guests(guest_repository):
    TOTAL_GUESTS = 10
    guests = guest_repository.list_all()
    assert len(guests) == TOTAL_GUESTS


def test_list_all_guests_2_per_page(guest_repository):
    TOTAL_GUESTS = 2
    guests = guest_repository.list_all(per_page=2)
    assert len(guests) == TOTAL_GUESTS


def test_list_all_out_range_return_0(guest_repository):
    TOTAL_GUESTS = 0
    guests = guest_repository.list_all(page=60, per_page=1)
    assert len(guests) == TOTAL_GUESTS


def test_not_found_guests_by_id(guest_repository):
    with pytest.raises(NoResultFound):
        guest_repository.find_by_id('01JA5EZ0BBQRGDX69PNTVG3N5E')


def test_find_guest_by_id(guest_repository):
    booking = guest_repository.find_by_id('01JAFQSB29MRH1AH1J6Z8GR8KR')
    assert booking


def test_create_guest(guest_repository, session):
    dto = GuestCreateDTO(
        document='122434556',
        name='Teste Guest',
        surname='Teste Testando',
        phone='47389111111',
        country='Brasil',
    )

    guest = Guest.create(dto)

    guest_repository.create(guest)

    guest_created = session.scalar(
        select(GuestDB).where(GuestDB.ulid == str(guest.ulid))
    )
    assert guest_created is not None
    assert guest_created.ulid == str(guest.ulid)


def test_update_guest(guest_repository):
    update_data = GuestUpdateDTO(name='Super Teste')

    updated_guest = guest_repository.update(
        '01JAFQT8BNX2K4SXH1TH6ESQFX', update_data
    )

    assert updated_guest.name == 'Super Teste'


def test_delete_guest(guest_repository, session):
    guest_repository.delete('01JAFQTH6ETC71168EYY8JX4WE')

    with pytest.raises(NoResultFound):
        session.get_one(GuestDB, '01JAFQTH6ETC71168EYY8JX4WE')
