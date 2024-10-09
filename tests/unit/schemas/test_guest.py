from app.schemas.Guest import Guest, GuestCreateDTO


def test_guest():
    dto = GuestCreateDTO(
        name='Bento',
        country='Brasil',
        document='1234567',
        phone='4599920343',
        surname='Machado',
    )
    guest = Guest.create(dto)
    assert guest.document == '1234567'
