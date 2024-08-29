from app.domain.Accommodation import Accommodation, AccommodationCreateDTO
from app.domain.Amenitie import Amenitie


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

    accommodation = Accommodation(
        amenities=[
            Amenitie(name=amenitie) for amenitie in accommodation_dto.amenities
        ],
        double_beds=accommodation_dto.double_beds,
        name=accommodation_dto.name,
        price=accommodation_dto.price,
        single_beds=accommodation_dto.single_beds,
        status=accommodation_dto.status,
        total_guests=accommodation_dto.total_guests,
    )

    assert accommodation
    assert hasattr(accommodation, 'id')
    assert hasattr(accommodation, 'created_at')
