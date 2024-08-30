from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infra.database.models import BookingDB


def list_all_bookings(session: Session):
    bookings = tuple(session.scalars(select(BookingDB)).all())

    return bookings
