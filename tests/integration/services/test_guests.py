from uuid import UUID

from sqlalchemy import select

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO
from app.services.guests import create, delete, find_by_id, list_all, update


def test_list_all_guests(session):
    guests = list_all(session)
    assert len(guests) == 1
    assert guests[0].name == 'Bento'


def test_create_new_guest(session):
    guest = GuestCreateDTO(
        document='31578421514',
        name='Astrubal',
        surname='Lima',
        phone='48923568741',
        country='Brasil',
    )

    create(session, guest)
    guests = session.scalars(select(GuestDB)).all()
    assert len(guests) == 2  # noqa: PLR2004
    assert guests[1].name == 'Astrubal'


def test_find_guest_by_id(session):
    guest = find_by_id(session, UUID('b73e37e2-ddca-4bec-86a9-016b5341c36f'))
    assert isinstance(guest, GuestDB)
    assert guest.name == 'Bento'


def test_update_guest(session):
    data = GuestUpdateDTO(phone='48974521254')
    updated_guest = update(
        session, UUID('b73e37e2-ddca-4bec-86a9-016b5341c36f'), data
    )
    assert isinstance(updated_guest, GuestDB)
    assert updated_guest.phone == '48974521254'


def test_delete_guest(session):
    delete(session, UUID('b73e37e2-ddca-4bec-86a9-016b5341c36f'))

    error = delete(session, UUID('b73e37e2-ddca-4bec-86a9-016b5341c36f'))
    assert isinstance(error, NotFoundError)


# TODO: Testar casos de erros
