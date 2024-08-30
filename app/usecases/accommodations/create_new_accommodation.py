from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import AccommodationDB, AmenitieDB
from app.schemas.Accommodation import AccommodationCreateDTO


def create_new_accommodation(
    session: Session, accommodation: AccommodationCreateDTO
):
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
