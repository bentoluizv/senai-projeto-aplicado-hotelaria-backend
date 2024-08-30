from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infra.database.models import GuestDB


def list_all_guests(session: Session):
    guests = tuple(session.scalars(select(GuestDB)).all())

    return guests
