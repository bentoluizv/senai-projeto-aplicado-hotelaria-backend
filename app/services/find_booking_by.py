from typing import TypedDict

from app.data.repositories.BookingRepository import BookingRepository
from app.services.dto.BookingDTO import BookingDTO


class Input(TypedDict):
    id: str


class Output(TypedDict):
    booking: BookingDTO


def find_booking_by(
    bookingRepository: BookingRepository,
    input: Input,
) -> Output:
    existing_booking = bookingRepository.findBy("uuid", input["id"])

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

    return {"booking": booking_dto}
