from typing import TypedDict

from app.data.repositories.BookingRepository import BookingRepository
from app.services.dto.BookingDTO import BookingDTO


class Output(TypedDict):
    bookings: list[BookingDTO]


def list_all_bookings(bookingRepository: BookingRepository) -> Output:
    existing_bookings = bookingRepository.find_many()
    result: list[BookingDTO] = []
    for existing_booking in existing_bookings:
        booking_dto: BookingDTO = {
            "uuid": existing_booking.uuid,
            "created_at": existing_booking.created_at,
            "status": existing_booking.status,
            "guest_name": existing_booking.guest.name,
            "guest_phone": existing_booking.guest.phone,
            "accommodation_name": existing_booking.accommodation.name,
            "accommodation_price": str(existing_booking.accommodation.price),
            "check_in": existing_booking.check_in,
            "check_out": existing_booking.check_out,
            "total": str(existing_booking.calculate_budget()),
            "total_nights": str(existing_booking.calculate_period()),
        }
        result.append(booking_dto)

    return {"bookings": result}
