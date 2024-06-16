from typing import TypedDict

from app.data.repositories.BookingRepository import BookingRepository
from app.data.repositories.GuestRepository import GuestRepository


class Input(TypedDict):
    guest_document: str


def find_bookings_by_guest(
    bookingRepository: BookingRepository,
    guestRepository: GuestRepository,
    input: Input,
):
    guest = guestRepository.findBy("document", input["guest_document"])
    existing_bookings = bookingRepository.find_many()

    filtered_bookings = []

    for existing_booking in existing_bookings:
        if existing_booking.guest.name == guest.name:
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
            filtered_bookings.append(booking_dto)

    return {"bookings": filtered_bookings}
