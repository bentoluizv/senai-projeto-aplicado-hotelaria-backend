from uuid import UUID

from sqlalchemy.orm import Session

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import GuestDB


def find_guest_by_id(session: Session, id: str):
    uuid = UUID(id)

    existing_guest = session.get(GuestDB, uuid)

    if not existing_guest:
        raise NotFoundError(uuid)

    return existing_guest
