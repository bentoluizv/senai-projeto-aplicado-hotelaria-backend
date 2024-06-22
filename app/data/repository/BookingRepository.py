from typing import Any

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.BookingDAO import BookingDAO
from app.data.dao.GuestDAO import GuestDAO
from app.data.dao.schemas.BookingSchema import (
    BookingCreationalSchema,
    BookingDB,
)
from app.domain.Accommodation import Accommodation
from app.domain.Booking import Booking
from app.domain.Guest import Guest
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class BookingRepository:
    def __init__(
        self,
        booking_dao: BookingDAO,
        accommodation_dao: AccommodationDAO,
        guest_dao: GuestDAO,
    ):
        self.booking_dao = booking_dao
        self.accommodation_dao = accommodation_dao
        self.guest_dao = guest_dao

    def find_many(self) -> list[Booking]:
        bookings_db = self.booking_dao.find_many()

        bookings: list[Booking] = []

        for booking_db in bookings_db:
            guest_db = self.guest_dao.find(booking_db.guest_document)
            accommodation_db = self.accommodation_dao.find(
                booking_db.accommodation_id
            )

            if not guest_db or not accommodation_db:
                raise NotFoundError()

            booking_data = {
                'uuid': booking_db.uuid,
                'locator': booking_db.locator,
                'status': booking_db.status,
                'created_at': booking_db.created_at,
                'check_in': booking_db.check_in,
                'check_out': booking_db.check_out,
                'guest': Guest(**guest_db.model_dump()),
                'accommodation': Accommodation(
                    **accommodation_db.model_dump()
                ),
                'budget': booking_db.budget,
            }

            booking = Booking(**booking_data)
            bookings.append(booking)

        return bookings

    def find(self, uuid: str):
        booking_db = self.booking_dao.find(uuid)

        if not booking_db:
            raise NotFoundError()

        guest_db = self.guest_dao.find(booking_db.guest_document)
        accommodation_db = self.accommodation_dao.find(
            booking_db.accommodation_id
        )

        if not guest_db or not accommodation_db:
            raise NotFoundError()

        booking_data = {
            'uuid': booking_db.uuid,
            'locator': booking_db.locator,
            'status': booking_db.status,
            'created_at': booking_db.created_at,
            'check_in': booking_db.check_in,
            'check_out': booking_db.check_out,
            'guest': Guest(**guest_db.model_dump()),
            'accommodation': Accommodation(**accommodation_db.model_dump()),
            'budget': booking_db.budget,
        }

        return Booking(**booking_data)

    def find_by(self, property: str, value: str):
        bookings_db = self.booking_dao.find_by(property, value)

        if not bookings_db:
            raise NotFoundError()

        bookings: list[Booking] = []

        for booking_db in bookings_db:
            guest_db = self.guest_dao.find(booking_db.guest_document)
            accommodation_db = self.accommodation_dao.find(
                booking_db.accommodation_id
            )

            if not guest_db or not accommodation_db:
                raise NotFoundError()

            booking_data = {
                'uuid': booking_db.uuid,
                'locator': booking_db.locator,
                'status': booking_db.status,
                'created_at': booking_db.created_at,
                'check_in': booking_db.check_in,
                'check_out': booking_db.check_out,
                'guest': Guest(**guest_db.model_dump()),
                'accommodation': Accommodation(
                    **accommodation_db.model_dump()
                ),
                'budget': booking_db.budget,
            }
            booking = Booking(**booking_data)
            bookings.append(booking)

        return bookings

    def create(self, data: dict[str, Any]):
        booking_data = BookingCreationalSchema(**data)
        exists = self.booking_dao.find_by('locator', booking_data.locator)

        if exists:
            raise AlreadyExistsError()

        guest_db = self.guest_dao.find(booking_data.guest_document)
        accommodation_db = self.accommodation_dao.find(
            booking_data.accommodation_id
        )

        if not guest_db or not accommodation_db:
            raise NotFoundError()

        self.booking_dao.create(booking_data)

    def update(self, data: dict[str, Any]):
        booking = BookingDB(**data)
        exists = self.booking_dao.find(booking.uuid)

        if not exists:
            raise NotFoundError()

        self.booking_dao.update(booking)

    def delete(self, uuid: str):
        exists = self.booking_dao.find(uuid)

        if not exists:
            raise NotFoundError()

        self.booking_dao.delete(uuid)
