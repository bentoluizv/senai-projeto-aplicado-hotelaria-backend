from datetime import datetime

from ulid import ULID

from app.schemas.Accommodation import Accommodation, AccommodationCreateDTO
from app.schemas.Booking import Booking, BookingCreateDTO
from app.schemas.Guest import Guest, GuestCreateDTO


def test_booking():
    u = ULID()

    booking_dto = BookingCreateDTO(
        check_in=datetime(2024, 3, 12, 6, 30),
        check_out=datetime(2024, 3, 14, 17, 30),
        guest_document='123792834',
        accommodation_ulid=str(u),
    )

    guest_dto = GuestCreateDTO(
        name='Bento',
        country='Brasil',
        document='123792834',
        phone='4599920343',
        surname='Machado',
    )

    accommodation_dto = AccommodationCreateDTO(
        name='teste',
        status='disponível',
        total_guests=1,
        single_beds=0,
        double_beds=1,
        price=70,
        amenities=['wifi', 'banheira'],
    )

    guest = Guest.create(guest_dto)
    accommodation = Accommodation.create(accommodation_dto)
    accommodation.ulid = u

    booking = Booking.create(booking_dto, guest, accommodation)
    assert booking.accommodation.ulid == accommodation.ulid
    assert booking.guest.surname == 'Machado'
