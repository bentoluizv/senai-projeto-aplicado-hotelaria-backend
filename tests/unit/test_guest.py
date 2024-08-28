from datetime import datetime
from uuid import UUID

from app.data.database.models import GuestDB
from app.domain.Guest import Guest, GuestCreateDTO


def test_should_create_a_new_guest_from_dto():
    guest_dto = GuestCreateDTO(
        name='Teste2',
        surname='Super Teste',
        document='123456789',
        country='Argentina',
        phone='48922554872',
    )

    guest = Guest.create(guest_dto)

    assert hasattr(guest, 'uuid')
    assert hasattr(guest, 'created_at')


def test_should_create_a_new_guest_from_db_obj():
    guest_db = GuestDB(
        uuid=UUID('0bc4184a-e3ff-45c0-8514-98e47180c837'),
        created_at=datetime(2024, 8, 1),
        name='Teste2',
        surname='Super Teste',
        document='123456789',
        country='Argentina',
        phone='48922554872',
    )

    guest = Guest.from_database(guest_db)

    assert guest.uuid == UUID('0bc4184a-e3ff-45c0-8514-98e47180c837')
