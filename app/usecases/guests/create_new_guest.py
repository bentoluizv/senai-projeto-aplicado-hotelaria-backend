from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO


def create_new_guest(session: Session, guest: GuestCreateDTO):
    existing_guest = session.scalar(
        select(GuestDB).where(GuestDB.document == guest.document)
    )

    if existing_guest:
        raise AlreadyExistsError(guest.document)

    new_db_guest = GuestDB(
        country=guest.country,
        document=guest.document,
        name=guest.name,
        phone=guest.phone,
        surname=guest.surname,
    )

    session.add(new_db_guest)

    session.commit()
