from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import AccommodationDB, AmenitieDB
from app.schemas.Accommodation import (
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)


def create(session: Session, accommodation: AccommodationCreateDTO):
    existing_accommodation = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == accommodation.name
        )
    )

    if existing_accommodation:
        raise AlreadyExistsError(accommodation.name)

    db_amenities: list[AmenitieDB] = []

    for amenitie in accommodation.amenities:
        existing_amenitie = session.scalar(
            select(AmenitieDB).where(AmenitieDB.name == amenitie)
        )

        if not existing_amenitie:
            raise NotFoundError(amenitie)

        db_amenities.append(existing_amenitie)

    new_db_accommodation = AccommodationDB(
        name=accommodation.name,
        amenities=db_amenities,
        double_beds=accommodation.double_beds,
        price=accommodation.price,
        single_beds=accommodation.single_beds,
        status=accommodation.status,
        total_guests=accommodation.total_guests,
    )

    session.add(new_db_accommodation)

    session.commit()


def list_all(session: Session):
    accommodations = session.scalars(select(AccommodationDB)).all()

    return accommodations


def find_by_id(session: Session, id: str):
    existing_accommodation = session.get(AccommodationDB, id)

    if not existing_accommodation:
        raise NotFoundError(id)

    return existing_accommodation


def update(session: Session, id: str, data: AccommodationUpdateDTO):
    existing_accommodation = session.get(AccommodationDB, id)

    if not existing_accommodation:
        raise NotFoundError(id)

    for key, value in data.model_dump().items():
        if value:
            setattr(existing_accommodation, key, value)

    session.commit()
    session.refresh(existing_accommodation)

    return existing_accommodation


def delete(session: Session, id: str):
    existing_accommodation = session.get(AccommodationDB, id)

    if not existing_accommodation:
        raise NotFoundError(id)

    session.delete(existing_accommodation)
    session.commit()
