from typing import Annotated

from fastapi import Depends

from app.database.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.database.repositories.BookingRepository import BookingRepository
from app.database.repositories.GuestRepository import GuestRepository
from app.entities.Booking import Booking, BookingCreateDTO, BookingUpdateDTO
from app.errors.ConflictBookingError import ConflictBookingError
from app.errors.NotFoundError import NotFoundError
from app.errors.OutOfRangeError import OutOfRangeError
from app.factory.RepositoryFactory import RepositoryFactory


class BookingController:
    booking_repository: BookingRepository
    guest_repository: GuestRepository
    accommodation_repository: AccommodationRepository

    def __init__(
        self,
        repository_factory: Annotated[
            RepositoryFactory, Depends(RepositoryFactory)
        ],
    ) -> None:
        self.booking_repository = (
            repository_factory.create_booking_respository()
        )
        self.guest_repository = repository_factory.create_guest_respository()
        self.accommodation_repository = (
            repository_factory.create_accommodation_respository()
        )

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Booking]:
        total_bookings = self.booking_repository.count()

        if total_bookings == 0:
            return []

        total_pages = (total_bookings + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            raise OutOfRangeError(page, total_pages)
        bookings = self.booking_repository.list_all(page, per_page)

        return bookings

    def find_by_id(self, id: str):
        booking = self.booking_repository.find_by_id(id)

        if not booking:
            raise NotFoundError('Booking', id)

        return booking

    def create(self, dto: BookingCreateDTO):
        guest = self.guest_repository.find_by_document(dto.guest_document)
        accommodation = self.accommodation_repository.find_by_id(
            dto.accommodation_ulid
        )

        if not accommodation:
            raise NotFoundError('Accommodtion', dto.accommodation_ulid)

        if not guest:
            raise NotFoundError('Guest', dto.guest_document)

        is_in_conflict = self.booking_repository.is_in_conflict(
            dto.check_in, dto.check_out
        )

        if is_in_conflict:
            raise ConflictBookingError('Booking', dto.check_in, dto.check_out)

        booking = Booking.create(dto, guest, accommodation)

        self.booking_repository.create(booking)

    def update(self, id: str, dto: BookingUpdateDTO):
        existing = self.booking_repository.find_by_id(id)

        if not existing:
            raise NotFoundError('Booking', id)

        self.booking_repository.update(id, dto)

    def delete(self, id: str):
        existing = self.booking_repository.find_by_id(id)

        if not existing:
            raise NotFoundError('Booking', id)

        self.booking_repository.delete(id)
