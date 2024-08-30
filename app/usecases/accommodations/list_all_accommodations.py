from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infra.database.models import AccommodationDB


def list_all_accommodations(session: Session):
    accommodations = tuple(session.scalars(select(AccommodationDB)).all())

    return accommodations
