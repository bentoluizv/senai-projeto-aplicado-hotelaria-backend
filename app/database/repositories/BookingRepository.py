from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session

from app.database.models import (
    AccommodationDB,
    BookingDB,
    GuestDB,
)
from app.entities.Booking import Booking
from app.entities.schemas.ListSettings import ListSettings, Pagination


class BookingRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        total_bookings = self.session.scalar(
            select(func.count()).select_from(BookingDB)
        )

        return total_bookings or 0

    def count_by_guest(self, guest_ulid: str) -> int:
        total_bookings = self.session.scalar(
            select(func.count())
            .select_from(BookingDB)
            .where(BookingDB.guest_ulid == guest_ulid)
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

    def list_all(
        self, settings: ListSettings = ListSettings(pagination=Pagination())
    ) -> list[Booking]:
        offset = (settings.pagination.page - 1) * settings.pagination.per_page

        query = (
            select(BookingDB)
            .order_by(desc(BookingDB.ulid))
            .limit(settings.pagination.per_page)
            .offset(offset)
        )

        if settings.filter:
            query = (
                select(BookingDB)
                .where(
                    and_(
                        BookingDB.check_in <= settings.filter.check_out,
                        BookingDB.check_out >= settings.filter.check_in,
                    )
                )
                .order_by(BookingDB.check_in)
                .limit(settings.pagination.per_page)
                .offset(offset)
            )

        db_bookings = self.session.scalars(query).all()

        bookings = [Booking.from_db(db_booking) for db_booking in db_bookings]

        return bookings

    def list_all_by_guest(
        self,
        guest_ulid: str,
        settings: ListSettings = ListSettings(pagination=Pagination()),
    ) -> list[Booking]:
        offset = (settings.pagination.page - 1) * settings.pagination.per_page

        query = (
            select(BookingDB)
            .where(BookingDB.guest_ulid == guest_ulid)
            .order_by(desc(BookingDB.ulid))
            .limit(settings.pagination.per_page)
            .offset(offset)
        )

        if settings.filter:
            query = (
                select(BookingDB)
                .where(BookingDB.guest_ulid == guest_ulid)
                .where(
                    and_(
                        BookingDB.check_in <= settings.filter.check_out,
                        BookingDB.check_out >= settings.filter.check_in,
                    )
                )
                .order_by(BookingDB.check_in)
                .limit(settings.pagination.per_page)
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

    def is_in_conflict(self, booking: Booking) -> bool:
        return (
            self.session.scalars(
                select(BookingDB)
                .filter(
                    BookingDB.accommodation_ulid
                    == str(booking.accommodation.ulid),
                    BookingDB.check_in < booking.check_out,
                    BookingDB.check_out > booking.check_in,
                )
                .order_by(BookingDB.check_in)
            ).first()
            is not None
        )
