from app.domain.Guest import Guest, GuestCreateDTO


def test_should_create_a_new_guest_from_dto():
    guest_dto = GuestCreateDTO(
        name='Teste2',
        surname='Super Teste',
        document='123456789',
        country='Argentina',
        phone='48922554872',
    )

    guest = Guest(**guest_dto.model_dump())

    assert hasattr(guest, 'uuid')
    assert hasattr(guest, 'created_at')
