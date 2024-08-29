from datetime import datetime

from app.data.database.models import AccommodationDB, AmenitieDB
from app.domain.Accommodation import Accommodation, AccommodationCreateDTO


def test_should_create_a_new_accommodation_from_dto():
    accommodation_dto = AccommodationCreateDTO(
        status='Disponivel',
        amenities=['ar-condicionado'],
        double_beds=2,
        price=250,
        single_beds=1,
        total_guests=3,
        name='Quarto de Testes',
    )

    accommodation = Accommodation.create(accommodation_dto)

    assert accommodation
    assert hasattr(accommodation, 'id')
    assert hasattr(accommodation, 'created_at')


def test_should_create_a_new_accommodation_from_db_obj():
    accommodation_db = AccommodationDB(
        created_at=datetime.now(),
        status='Disponivel',
        amenities=[AmenitieDB(name='WIFI')],
        double_beds=2,
        price=250,
        single_beds=1,
        total_guests=3,
        name='Quarto de Testes',
    )

    accommodation = Accommodation.from_database(accommodation_db)

    assert accommodation.name == 'Quarto de Testes'
    assert hasattr(accommodation, 'id')
    assert hasattr(accommodation, 'created_at')
