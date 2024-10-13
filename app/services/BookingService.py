from http import HTTPStatus

from fastapi import HTTPException

from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.infra.repositories.BookingRepository import BookingRepository
from app.infra.repositories.GuestRepository import GuestRepository
from app.schemas.Booking import (
    Booking,
    BookingCreateDTO,
    BookingUpdateDTO,
    Status,
)


class BookingService:
    guest_repository: GuestRepository
    accommodation_repository: AccommodationRepository
    booking_repository: BookingRepository

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.booking_repository = (
            repository_factory.create_booking_repository()
        )
        self.guest_repository = repository_factory.create_guest_repository()
        self.accommodation_repository = (
            repository_factory.create_accommodation_repository()
        )

    def create_new_booking(self, dto: BookingCreateDTO):
        guest = self.guest_repository.find_by_document(dto.guest_document)

        if not guest:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Guest with document {dto.guest_document} not found',
            )

        accommodation = self.accommodation_repository.find_by_id(
            dto.accommodation_ulid
        )

        if not accommodation:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Id {dto.accommodation_ulid} not found',
            )

        is_in_conflict = self.booking_repository.is_in_conflict(
            dto.check_in, dto.check_out
        )

        if is_in_conflict:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Checkin/Checkout is conflicting with another booking',
            )
        booking = Booking.create(dto, guest, accommodation)
        self.booking_repository.create(booking)

    def find_by_id(self, id: str):
        existing_booking = self.booking_repository.find_by_id(id)

        if not existing_booking:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'Id {id} not found'
            )

        return existing_booking

    def list_all(self, page: int = 1, per_page: int = 10):
        if page > self.booking_repository.info.total_pages:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='page out of range'
            )

        bookings = self.booking_repository.list_all(page, per_page)

        return bookings

    def _is_booking_status_updatable(
        self, actual: Status, new_status: Status
    ) -> bool:
        if actual == Status.CANCELED:
            return False

        if actual == Status.COMPLETED:
            return False

        if actual == Status.BOOKED:
            allowed_next_status = [Status.CANCELED, Status.WAITING_CHECK_IN]
            if new_status not in allowed_next_status:
                return False

        if actual == Status.WAITING_CHECK_IN:
            allowed_next_status = [Status.WAITING_CHECK_OUT]
            if new_status not in allowed_next_status:
                return False

        if actual == Status.WAITING_CHECK_OUT:
            allowed_next_status = [Status.COMPLETED]
            if new_status not in allowed_next_status:
                return False

        return True

    def update_status(self, id: str, status: Status):
        booking = self.booking_repository.find_by_id(id)

        if not booking:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'ID {id} not found!'
            )

        updatable = self._is_booking_status_updatable(booking.status, status)

        if not updatable:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Booking Status not updatable',
            )

        self.booking_repository.update_status(id, status)

    def update_data(self, id: str, dto: BookingUpdateDTO):
        booking = self.booking_repository.find_by_id(id)

        if not booking:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'ID {id} not found!'
            )

        if booking.status != Status.BOOKED:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Booking is not updatable',
            )

        self.booking_repository.update(id, dto)
