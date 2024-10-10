from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infra.database.models import AmenitieDB
from app.schemas.Amenitie import Amenitie, AmenitieCreateDTO


class AmenitieRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, amenitie: AmenitieCreateDTO):
        db_amenitie = AmenitieDB(
            name=amenitie.name,
        )
        self.session.add(db_amenitie)
        self.session.commit()

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Amenitie]:
        offset = (page - 1) * per_page
        db_amenities = self.session.scalars(
            select(AmenitieDB).limit(per_page).offset(offset)
        )
        amenities = [
            Amenitie(name=db_amenitie.name) for db_amenitie in db_amenities
        ]
        return amenities
