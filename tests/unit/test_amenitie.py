from app.data.database.models import AmenitieDB
from app.domain.Amenitie import Amenitie, AmenitieCreateDTO


def test_should_create_a_new_amenitie_from_dto():
    amenitie_dto = AmenitieCreateDTO(
        name='Ar Condicionado',
    )

    amenitie = Amenitie.create(amenitie_dto)

    assert amenitie


def test_should_create_a_new_amenitie_from_db_obj():
    guest_db = AmenitieDB(
        name='Teste2',
    )

    amenitie = Amenitie.from_database(guest_db)

    assert amenitie.name == 'Teste2'
    assert hasattr(amenitie, 'id')
