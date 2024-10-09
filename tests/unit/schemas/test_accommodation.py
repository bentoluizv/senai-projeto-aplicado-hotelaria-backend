from app.schemas.Accommodation import Accommodation, AccommodationCreateDTO


def test_accommodation():
    dto = AccommodationCreateDTO(
        name='teste',
        status='disponível',
        total_guests=1,
        single_beds=0,
        double_beds=1,
        price=70,
        amenities=['wifi', 'banheira'],
    )
    accommodatio = Accommodation.create(dto)
    assert accommodatio.name == 'teste'
