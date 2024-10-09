from app.schemas.Amenitie import Amenitie, AmenitieCreateDTO


def test_amenitie():
    dto = AmenitieCreateDTO(name='wifi')
    amenitie = Amenitie.create(dto)
    assert amenitie.name == 'wifi'
