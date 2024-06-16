from typing import TypedDict

from app.data.repositories.BookingRepository import BookingRepository


class Input(TypedDict):
    key: str
    value: str


def find_booking_by(
    bookingRepository: BookingRepository,
    input: Input,
):
    existing_booking = bookingRepository.findBy(input["key"], input["value"])

    booking_dto = {
        "uuid": existing_booking.uuid,
        "created_at": existing_booking.created_at,
        "status": existing_booking.status,
        "guest": existing_booking.guest.to_dict(),
        "accommodation": existing_booking.accommodation.to_dict(),
        "check_in": existing_booking.check_in,
        "check_out": existing_booking.check_out,
        "total": str(existing_booking.calculate_budget()),
        "total_nights": str(existing_booking.calculate_period()),
    }

    return {"booking": booking_dto}
