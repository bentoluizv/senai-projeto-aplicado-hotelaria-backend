from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.database.models import AmenitieDB
from app.entities.Amenitie import Amenitie


class AmenitieRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        total_bookings = self.session.scalar(
            select(func.count()).select_from(AmenitieDB)
        )

        return total_bookings or 0

    def create(self, amenitie: Amenitie):
        db_amenitie = AmenitieDB(
            name=amenitie.name,
        )
        self.session.add(db_amenitie)
        self.session.commit()

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Amenitie]:
        offset = (page - 1) * per_page
        db_amenities = self.session.scalars(
            select(AmenitieDB)
            .limit(per_page)
            .offset(offset)
            .order_by(desc(AmenitieDB.id))
        )
        amenities = [
            Amenitie.from_db(db_amenitie) for db_amenitie in db_amenities
        ]
        return amenities

    def find_by_name(self, name: str) -> Amenitie | None:
        db_amenitie = self.session.scalar(
            select(AmenitieDB).where(AmenitieDB.name == name)
        )

        if not db_amenitie:
            return None

        amenitie = Amenitie(id=db_amenitie.id, name=db_amenitie.name)

        return amenitie

    def find_by_id(self, id: str) -> Amenitie | None:
        db_amenitie = self.session.scalar(
            select(AmenitieDB).where(AmenitieDB.id == id)
        )

        if not db_amenitie:
            return None

        amenitie = Amenitie(id=db_amenitie.id, name=db_amenitie.name)

        return amenitie

    def delete(self, id: int):
        db_guest = self.session.get_one(AmenitieDB, id)

        self.session.delete(db_guest)
        self.session.commit()
