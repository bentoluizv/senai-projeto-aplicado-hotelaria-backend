from typing import TypedDict

from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.data.repositories.BookingRepository import BookingRepository
from app.data.repositories.GuestRepository import GuestRepository
from app.entity.Booking import Booking


class Input(TypedDict):
    guest_document: str
    accommodation_id: str
    check_in: str
    check_out: str


class Output(TypedDict):
    uuid: str
    created_at: str
    locator: str


def create_new_booking(
    bookingRepository: BookingRepository,
    guestRepository: GuestRepository,
    accommodationRepository: AccommodationtRepository,
    input: Input,
) -> Output:
    guest = guestRepository.findBy("document", input["guest_document"])
    accommodation = accommodationRepository.findBy("id", input["accommodation_id"])

    booking_data = {
        "check_in": input["check_in"],
        "check_out": input["check_out"],
        "guest": guest,
        "accommodation": accommodation,
    }

    booking = Booking.from_dict(booking_data)

    # TODO: VALIDAR SE A ACOMODAÇÃO JÁ ESTÁ RESERVADA DURANTE O PERIODO DE ESTADIA

    bookingRepository.insert(booking)

    return {
        "uuid": booking.uuid,
        "created_at": booking.created_at,
        "locator": booking.get_locator(),
    }
