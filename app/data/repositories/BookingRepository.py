from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models import BookingDB
from app.domain.Booking import Booking, BookingCreateDTO, BookingUpdateDTO
from app.domain.errors.AlreadyExistsError import AlreadyExistsError
from app.domain.errors.NotFoundError import NotFoundError


class BookingRepository:
    def __init__(self, database: Session):
        self.database = database

    def list(self):
        db_bookings = self.database.scalars(select(BookingDB)).all()
        bookings = [
            Booking.from_database(db_booking) for db_booking in db_bookings
        ]

        return bookings

    def find_by_id(self, id: UUID):
        db_booking = self.database.get(BookingDB, id)

        if not db_booking:
            raise NotFoundError(id)

        booking = Booking.from_database(db_booking)

        return booking

    def insert(self, data: BookingCreateDTO):
        booking = Booking.create(data)
        exists = self.database.scalar(
            select(BookingDB).where(BookingDB.locator == booking.locator)
        )

        if exists:
            raise AlreadyExistsError(booking.locator)

        db_booking = BookingDB(**booking.model_dump())
        self.database.add(db_booking)
        self.database.commit()

    def update(self, id: UUID, data: BookingUpdateDTO):
        db_booking = self.database.get(BookingDB, id)

        if not db_booking:
            raise NotFoundError(id)

        for key, value in data.model_dump().items():
            if value is not None:
                setattr(db_booking, key, value)

        self.database.commit()

    def delete(self, uuid: UUID):
        db_booking = self.database.get(BookingDB, id)

        if not db_booking:
            raise NotFoundError(id)

        self.database.delete(db_booking)
