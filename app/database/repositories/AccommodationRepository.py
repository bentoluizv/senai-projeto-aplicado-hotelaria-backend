from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import AccommodationDB, AmenitieDB
from app.entities.Accommodation import (
    Accommodation,
    AccommodationUpdateDTO,
)


class AccommodationRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        total_accommodation = self.session.scalar(
            select(func.count()).select_from(AccommodationDB)
        )

        return total_accommodation or 0

    def create(self, accommodation: Accommodation) -> None:
        db_amenities: list[AmenitieDB] = []

        for amenitie in accommodation.amenities:
            existing_amenitie = self.session.scalar(
                select(AmenitieDB).where(AmenitieDB.name == amenitie)
            )

            if existing_amenitie:
                db_amenities.append(existing_amenitie)

        db_accommodation = AccommodationDB(
            name=accommodation.name,
            double_beds=accommodation.double_beds,
            price=accommodation.price,
            single_beds=accommodation.single_beds,
            total_guests=accommodation.total_guests,
            status=accommodation.status.value,
        )

        db_accommodation.amenities = db_amenities

        self.session.add(db_accommodation)
        self.session.commit()

    def list_all(
        self, page: int = 1, per_page: int = 10
    ) -> list[Accommodation]:
        offset = (page - 1) * per_page
        db_accommodations = self.session.scalars(
            select(AccommodationDB).limit(per_page).offset(offset)
        )

        accommodations = [
            Accommodation.from_db(db_accommodation)
            for db_accommodation in db_accommodations
        ]

        return accommodations

    def find_by_id(self, id: str) -> Accommodation | None:
        db_accommodation = self.session.get(AccommodationDB, id)

        if not db_accommodation:
            return None

        accommodation = Accommodation.from_db(db_accommodation)
        return accommodation

    def find_by_name(self, name: str) -> Accommodation | None:
        db_accommodation = self.session.scalar(
            select(AccommodationDB).where(AccommodationDB.name == name)
        )
        if not db_accommodation:
            return None

        accommodation = Accommodation.from_db(db_accommodation)
        return accommodation

    def update(self, id: str, dto: AccommodationUpdateDTO) -> Accommodation:
        db_accommodation = self.session.get_one(AccommodationDB, id)

        for key, value in dto.model_dump().items():
            if value:
                setattr(db_accommodation, key, value)

        self.session.commit()
        self.session.refresh(db_accommodation)
        accommodation = Accommodation.from_db(db_accommodation)
        return accommodation

    def delete(self, id: str):
        db_accommodation = self.session.get_one(AccommodationDB, id)

        self.session.delete(db_accommodation)
        self.session.commit()
