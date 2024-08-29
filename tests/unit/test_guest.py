from datetime import datetime
from uuid import uuid4

from app.domain.Guest import Guest, GuestCreateDTO


def test_should_create_a_new_guest_from_dto():
    guest_dto = GuestCreateDTO(
        name='Teste2',
        surname='Super Teste',
        document='123456789',
        country='Argentina',
        phone='48922554872',
    )

    guest = Guest(
        country=guest_dto.country,
        created_at=datetime.now(),
        document=guest_dto.document,
        name=guest_dto.name,
        phone=guest_dto.phone,
        surname=guest_dto.surname,
        uuid=uuid4(),
    )

    assert hasattr(guest, 'uuid')
    assert hasattr(guest, 'created_at')
