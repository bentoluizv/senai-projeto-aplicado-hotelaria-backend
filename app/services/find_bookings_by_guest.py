from typing import TypedDict

from app.data.repositories.BookingRepository import BookingRepository
from app.data.repositories.GuestRepository import GuestRepository
from app.services.dto.BookingDTO import BookingDTO


class Input(TypedDict):
    guest_document: str


class Output(TypedDict):
    bookings: list[BookingDTO]


def find_bookings_by_guest(
    bookingRepository: BookingRepository,
    guestRepository: GuestRepository,
    input: Input,
) -> Output:
    guest = guestRepository.findBy("document", input["guest_document"])
    existing_bookings = bookingRepository.find_many()

    filtered_bookings: list[BookingDTO] = []

    for existing_booking in existing_bookings:
        if existing_booking.guest.name == guest.name:
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
            filtered_bookings.append(booking_dto)

    return {"bookings": filtered_bookings}
