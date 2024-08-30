from uuid import UUID

from sqlalchemy.orm import Session

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestUpdateDTO


def update_guest(session: Session, id: str, data: GuestUpdateDTO):
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
