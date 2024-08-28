from datetime import datetime
from uuid import UUID, uuid4

from app.data.database.models import (
    AccommodationDB,
    AmenitieDB,
    BookingDB,
    GuestDB,
)
from app.domain.Accommodation import Accommodation
from app.domain.Amenitie import Amenitie
from app.domain.Booking import (
    Booking,
    BookingCreateDTO,
    BookingDTOWithGuestAndAccommodation,
)
from app.domain.Guest import Guest


def test_should_create_a_new_booking_from_dto():
    booking_dto = BookingCreateDTO(
        accommodation_id=1,
        budget=2800,
        check_in=datetime(2024, 9, 12),
        check_out=datetime(2024, 9, 18),
        guest_document='00157624242',
        status='Aguardando Check-in',
    )

    booking_with_guests_and_accommodation = (
        BookingDTOWithGuestAndAccommodation(
            **booking_dto.model_dump(),
            guest=Guest(
                document=booking_dto.guest_document,
                name='Bento',
                surname='Machado',
                country='Brasil',
                phone='4899205142',
            ),
            accommodation=Accommodation(
                id=booking_dto.accommodation_id,
                status='Disponivel',
                amenities=[Amenitie(name='ar-condicionado')],
                double_beds=2,
                price=250,
                single_beds=1,
                total_guests=3,
                name='Quarto de Testes',
            ),
        )
    )

    booking = Booking.create(booking_with_guests_and_accommodation)

    assert booking
    assert hasattr(booking, 'uuid')
    assert hasattr(booking, 'created_at')
    assert Amenitie(name='ar-condicionado') in booking.accommodation.amenities
    assert booking.guest.name == 'Bento'
    assert booking.accommodation.name == 'Quarto de Testes'


def test_should_create_a_new_booking_from_db_obj():
    booking_db = BookingDB(
        uuid=uuid4(),
        locator='XLA12458',
        created_at=datetime.now(),
        status='Aguardando Check-in',
        budget=2800,
        check_in=datetime(2024, 9, 12),
        check_out=datetime(2024, 9, 18),
        accommodation=AccommodationDB(
            created_at=datetime.now(),
            status='Disponivel',
            amenities=[AmenitieDB(name='WIFI')],
            double_beds=2,
            price=250,
            single_beds=1,
            total_guests=3,
            name='Quarto de Testes',
        ),
        guest=GuestDB(
            uuid=UUID('0bc4184a-e3ff-45c0-8514-98e47180c837'),
            created_at=datetime(2024, 8, 1),
            name='Teste2',
            surname='Super Teste',
            document='123456789',
            country='Argentina',
            phone='48922554872',
        ),
    )

    booking = Booking.from_database(booking_db)

    assert booking.locator == 'XLA12458'
    assert isinstance(booking.guest, Guest)
    assert isinstance(booking.accommodation, Accommodation)
