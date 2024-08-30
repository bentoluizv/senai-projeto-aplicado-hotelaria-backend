from sqlalchemy.orm import Session

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import AccommodationDB
from app.schemas.Accommodation import AccommodationUpdateDTO


def update_accommodation(
    session: Session, id: str, data: AccommodationUpdateDTO
):
    existing_accommodation = session.get(AccommodationDB, id)

    if not existing_accommodation:
        raise NotFoundError(id)

    for key, value in data.model_dump().items():
        if value:
            setattr(existing_accommodation, key, value)

    session.commit()
    session.refresh(existing_accommodation)

    return existing_accommodation
