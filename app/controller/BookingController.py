from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound

from app.database.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.database.repositories.BookingRepository import BookingRepository
from app.database.repositories.GuestRepository import GuestRepository
from app.entities.Booking import Booking, BookingCreateDTO, BookingUpdateDTO
from app.errors.AlreadyExistsError import AlreadyExistsError
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

        total_pages = (total_bookings + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            raise OutOfRangeError(page, total_pages)
        bookings = self.booking_repository.list_all(page, per_page)

        return bookings

    def find_by_id(self, id: str):
        try:
            existing_booking = self.booking_repository.find_by_id(id)

            return existing_booking

        except NoResultFound:
            raise NotFoundError('Booking', id)

    def create(self, dto: BookingCreateDTO):
        try:
            guest = self.guest_repository.find_by_document(dto.guest_document)
            accommodation = self.accommodation_repository.find_by_id(
                dto.accommodation_ulid
            )
            booking = Booking.create(dto, guest, accommodation)
            self.booking_repository.create(booking)

        except NotFoundError as err:
            raise err

        except AlreadyExistsError as err:
            raise err

    def update(self, id: str, dto: BookingUpdateDTO):
        try:
            self.booking_repository.find_by_id(id)
            self.booking_repository.update(id, dto)

        except NoResultFound:
            raise NotFoundError('Booking', id)

    def delete(self, id: str):
        try:
            self.booking_repository.find_by_id(id)
            self.booking_repository.delete(id)

        except NoResultFound:
            raise NotFoundError('Booking', id)
