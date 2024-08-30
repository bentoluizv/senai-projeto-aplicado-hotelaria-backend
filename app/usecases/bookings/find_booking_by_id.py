from uuid import UUID

from sqlalchemy.orm import Session

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import BookingDB


def find_booking_by_id(session: Session, id: str):
    uuid = UUID(id)

    existing_booking = session.get(BookingDB, uuid)

    if not existing_booking:
        raise NotFoundError(uuid)

    return existing_booking
