from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import AmenitieDB
from app.entities.Amenitie import Amenitie


def get_amenities_from_db(
    amenities: list[Amenitie], session: Session
) -> list[AmenitieDB]:
    db_amenities: list[AmenitieDB] = []

    for amenitie in amenities:
        existing_amenitie = session.scalar(
            select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
        )

        if existing_amenitie:
            db_amenities.append(existing_amenitie)

    return db_amenities
