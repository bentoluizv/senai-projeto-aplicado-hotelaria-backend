from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import (
    AccommodationDB,
    BookingDB,
    GuestDB,
)
from app.entities.Booking import Booking


class BookingRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        total_bookings = self.session.scalar(
            select(func.count()).select_from(BookingDB)
        )

        return total_bookings or 0

    def create(self, booking: Booking) -> Booking:
        db_guest = self.session.get_one(GuestDB, str(booking.guest.ulid))

        db_accommodation = self.session.get_one(
            AccommodationDB, str(booking.accommodation.ulid)
        )

        db_booking = BookingDB(
            status=booking.status.value,
            check_in=booking.check_in,
            check_out=booking.check_out,
            budget=booking.budget,
            guest=db_guest,
            guest_ulid=db_guest.ulid,
            accommodation=db_accommodation,
            accommodation_ulid=db_accommodation.ulid,
        )

        self.session.add(db_booking)
        self.session.commit()

        created_booking = Booking.from_db(db_booking)
        return created_booking

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Booking]:
        offset = (page - 1) * per_page

        query = (
            select(BookingDB)
            .order_by(BookingDB.check_in)
            .limit(per_page)
            .offset(offset)
        )

        db_bookings = self.session.scalars(query).all()

        bookings = [Booking.from_db(db_booking) for db_booking in db_bookings]

        return bookings

    def find_by_id(self, id: str) -> Booking | None:
        db_booking = self.session.get(BookingDB, id)

        if not db_booking:
            return None

        booking = Booking.from_db(db_booking)

        return booking

    def update(self, booking: Booking) -> Booking:
        db_booking = self.session.get_one(BookingDB, str(booking.ulid))
        db_booking.status = booking.status.value
        self.session.add(db_booking)
        self.session.commit()
        self.session.refresh(db_booking)
        booking = Booking.from_db(db_booking)
        return booking

    def delete(self, id: str):
        db_booking = self.session.get_one(BookingDB, id)

        self.session.delete(db_booking)
        self.session.commit()

    def is_in_conflict(self, check_in: datetime, check_out: datetime) -> bool:
        conflict = self.session.scalars(
            select(BookingDB)
            .filter(
                BookingDB.check_in < check_out,
                BookingDB.check_out > check_in,
            )
            .order_by(BookingDB.check_in)
        ).first()

        if conflict:
            return True
        else:
            return False