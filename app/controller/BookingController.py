from typing import Annotated

from fastapi import Depends

from app.database.repositories.BookingRepository import BookingRepository
from app.entities.Booking import Booking
from app.errors.OutOfRangeError import OutOfRangeError
from app.factory.RepositoryFactory import RepositoryFactory


class BookingController:
    booking_repository: BookingRepository

    def __init__(
        self,
        repository_factory: Annotated[
            RepositoryFactory, Depends(RepositoryFactory)
        ],
    ) -> None:
        self.booking_repository = (
            repository_factory.create_booking_respository()
        )

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Booking]:
        total_bookings = self.booking_repository.count()

        total_pages = (total_bookings + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            raise OutOfRangeError(page, total_pages)
        bookings = self.booking_repository.list_all(page, per_page)

        return bookings
