from app.domain.Amenitie import Amenitie, AmenitieCreateDTO


def test_should_create_a_new_amenitie_from_dto():
    amenitie_dto = AmenitieCreateDTO(
        name='Ar Condicionado',
    )

    amenitie = Amenitie(**amenitie_dto.model_dump())

    assert amenitie
