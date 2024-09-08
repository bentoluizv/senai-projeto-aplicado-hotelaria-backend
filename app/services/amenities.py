from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.infra.database.models import AmenitieDB
from app.schemas.Amenitie import AmenitieCreateDTO


def create(session: Session, amenitie: AmenitieCreateDTO):
    existing_amenitie = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
    )

    if existing_amenitie:
        raise AlreadyExistsError(amenitie.name)

    new_db_amenitie = AmenitieDB(
        name=amenitie.name,
    )

    session.add(new_db_amenitie)

    session.commit()

def list_all(session: Session):
    amenities = session.scalars(select(AmenitieDB)).all()

    return amenities