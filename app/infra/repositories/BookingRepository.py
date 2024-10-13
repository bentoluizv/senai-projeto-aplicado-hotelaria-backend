from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.infra.models import AccommodationDB, BookingDB, GuestDB
from app.schemas.Booking import Booking, BookingUpdateDTO, Status
from app.schemas.Info import Info
from app.schemas.RepositorySettings import RepositorySettings


class BookingRepository:
    session: Session
    info: Info = Info()
    settings: RepositorySettings = RepositorySettings()

    def __init__(self, session: Session) -> None:
        self.session = session
        self._set_info()

    def _set_info(self):
        total = self.count()
        per_page = self.settings.pagination
        pages = (total + per_page - 1) // per_page
        self.info = Info(count=total, total_pages=pages)

    def count(self) -> int:
        total_bookings = self.session.scalar(
            select(func.count()).select_from(BookingDB)
        )

        return total_bookings or 0

    def create(self, booking: Booking):
        db_guest = self.session.get(GuestDB, str(booking.guest.ulid))
        db_accommodation = self.session.get(
            AccommodationDB, str(booking.accommodation.ulid)
        )
        if not db_guest or not db_accommodation or not booking.budget:
            raise None

        db_booking = BookingDB(
            ulid=str(booking.ulid),
            check_in=booking.check_in,
            check_out=booking.check_out,
            budget=booking.budget,
            guest=db_guest,
            accommodation=db_accommodation,
        )

        self.session.add(db_booking)
        self.session.commit()

    def list_all(self, page: int, per_page: int = 10) -> list[Booking]:
        offset = (page - 1) * per_page
        db_bookings = self.session.scalars(
            select(BookingDB)
            .order_by(BookingDB.check_in)
            .limit(per_page)
            .offset(offset)
        ).all()

        bookings = [Booking.from_db(db_booking) for db_booking in db_bookings]

        return bookings

    def find_by_id(self, id: str) -> Booking | None:
        db_booking = self.session.get(BookingDB, id)

        if not db_booking:
            return None

        booking = Booking.from_db(db_booking)

        return booking

    def update(self, id: str, dto: BookingUpdateDTO):
        db_booking = self.session.get(BookingDB, id)

        if not db_booking:
            return None

        for key, value in dto.model_dump().items():
            if value:
                setattr(db_booking, key, value)

        self.session.commit()

    def update_status(self, id: str, status: Status):
        db_booking = self.session.get(BookingDB, id)

        if not db_booking:
            return None

        db_booking.status = status

        self.session.commit()

    def delete(self, id: str):
        db_booking = self.session.get(BookingDB, id)

        if not db_booking:
            return None

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
