from datetime import datetime
from uuid import uuid4

from app.domain.Accommodation import Accommodation
from app.domain.Amenitie import Amenitie
from app.domain.Booking import (
    Booking,
    BookingCreateDTO,
)
from app.domain.Guest import Guest
from app.utils.generate_locator import generate_locator


def test_should_create_a_new_booking_from_dto():
    booking_dto = BookingCreateDTO(
        accommodation_id=1,
        budget=2800,
        check_in=datetime(2024, 9, 12),
        check_out=datetime(2024, 9, 18),
        guest_document='00157624242',
        status='Aguardando Check-in',
    )

    guest = Guest(
        uuid=uuid4(),
        created_at=datetime.now(),
        document=booking_dto.guest_document,
        name='Bento',
        surname='Machado',
        country='Brasil',
        phone='4899205142',
    )

    accommodation = Accommodation(
        id=booking_dto.accommodation_id,
        created_at=datetime.now(),
        status='Disponivel',
        amenities=[Amenitie(id=1, name='ar-condicionado')],
        double_beds=2,
        price=250,
        single_beds=1,
        total_guests=3,
        name='Quarto de Testes',
    )

    booking = Booking(
        uuid=uuid4(),
        created_at=datetime.now(),
        locator=generate_locator(),
        accommodation=accommodation,
        budget=booking_dto.budget,
        check_in=booking_dto.check_in,
        check_out=booking_dto.check_out,
        guest=guest,
        status=booking_dto.status,
    )

    assert booking
    assert hasattr(booking, 'uuid')
    assert hasattr(booking, 'created_at')
    assert (
        Amenitie(id=1, name='ar-condicionado')
        in booking.accommodation.amenities
    )
    assert booking.guest.name == 'Bento'
    assert booking.accommodation.name == 'Quarto de Testes'
