from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO


def create(session: Session, guest: GuestCreateDTO):
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


def find_by_id(session: Session, id: str):
    uuid = UUID(id)

    existing_guest = session.get(GuestDB, uuid)

    if not existing_guest:
        raise NotFoundError(uuid)

    return existing_guest


def list_all(session: Session):
    guests = session.scalars(select(GuestDB)).all()

    return guests


def update(session: Session, id: str, data: GuestUpdateDTO):
    uuid = UUID(id)

    existing_guest = session.get(GuestDB, uuid)

    if not existing_guest:
        raise NotFoundError(uuid)

    for key, value in data.model_dump().items():
        if value:
            setattr(existing_guest, key, value)

    session.commit()
    session.refresh(existing_guest)

    return existing_guest


def delete(session: Session, id: str):
    uuid = UUID(id)

    existing_guest = session.get(GuestDB, uuid)

    if not existing_guest:
        raise NotFoundError(uuid)

    session.delete(existing_guest)
    session.commit()
