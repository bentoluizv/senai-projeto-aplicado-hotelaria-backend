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
    existing = guest_repository.find_by_id('<nonexistentid>')
    assert not existing


def test_find_guest_by_id(guest_repository):
    guest = guest_repository.find_by_id('01JB3HNWQ2D7XPPJ181G3YTH8T')
    assert guest.name == 'John'


def test_find_guest_by_document(guest_repository):
    guest = guest_repository.find_by_document('3456547')
    assert guest.name == 'Alice'


def test_not_found_guests_by_document(guest_repository):
    existing = guest_repository.find_by_document('<document>')
    assert not existing


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
        select(GuestDB).where(GuestDB.name == str(guest.name))
    )
    assert guest_created is not None


def test_update_guest(guest_repository):
    update_data = GuestUpdateDTO(name='Super Teste')

    updated_guest = guest_repository.update(
        '01JB3HNWQ2D7XPPJ181G3YTH8T', update_data
    )

    assert updated_guest.name == 'Super Teste'


def test_delete_guest(guest_repository, session):
    guest_repository.delete('01JB3HNWQ2D7XPPJ181G3YTH8T')

    with pytest.raises(NoResultFound):
        session.get_one(GuestDB, '01JB3HNWQ2D7XPPJ181G3YTH8T')


def test_create_2_guests_in_a_row(guest_repository, session):
    dtos = [
        GuestCreateDTO(
            document='122434556',
            name='Teste Guest',
            surname='Teste Testando',
            phone='47389111111',
            country='Brasil',
        ),
        GuestCreateDTO(
            document='83792847',
            name='Teste Guest 2',
            surname='Teste Testando',
            phone='47389111111',
            country='Brasil',
        ),
    ]

    guests = [Guest.create(dto) for dto in dtos]

    for guest in guests:
        guest_repository.create(guest)

    db_guest_1 = session.scalar(
        select(GuestDB).where(GuestDB.document == guest.document)
    )
    db_guest_2 = session.scalar(
        select(GuestDB).where(GuestDB.document == guest.document)
    )
    assert db_guest_1
    assert db_guest_2
