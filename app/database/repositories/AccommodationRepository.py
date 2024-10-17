from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ulid import ULID

from app.database.models import AccommodationDB, AmenitieDB
from app.entities.Accommodation import (
    Accommodation,
    AccommodationUpdateDTO,
)
from app.errors.NotFoundError import NotFoundError


class AccommodationRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        if not self.session.is_active:
            raise Exception('A sessão do banco de dados está inativa.')

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
            ulid=str(ULID()),
            name=accommodation.name,
            double_beds=accommodation.double_beds,
            price=accommodation.price,
            single_beds=accommodation.single_beds,
            total_guests=accommodation.total_guests,
        )

        self.session.add(db_accommodation)
        self.session.commit()

    def list_all(self, page: int, per_page: int) -> list[Accommodation]:
        offset = (page - 1) * per_page
        db_accommodations = self.session.scalars(
            select(AccommodationDB).limit(per_page).offset(offset)
        )

        accommodations = [
            Accommodation.from_db(db_accommodation)
            for db_accommodation in db_accommodations
        ]

        return accommodations

    def find_by_id(self, id: str) -> Accommodation:
        db_accommodation = self.session.get(AccommodationDB, id)

        if not db_accommodation:
            raise NotFoundError('Accommodation', id)

        accommodation = Accommodation.from_db(db_accommodation)
        return accommodation

    def find_by_name(self, name: str) -> Accommodation | None:
        db_accommodation = self.session.scalar(
            select(AccommodationDB).where(AccommodationDB.name == name)
        )
        if not db_accommodation:
            raise NotFoundError('Accommodation', name)

        accommodation = Accommodation.from_db(db_accommodation)
        return accommodation

    def update(self, id: str, dto: AccommodationUpdateDTO):
        accommodation = self.session.get(AccommodationDB, id)

        for key, value in dto.model_dump().items():
            if value:
                setattr(accommodation, key, value)

        self.session.commit()

    def delete(self, id: str):
        db_accommodation = self.session.get(AccommodationDB, id)

        if not db_accommodation:
            raise NotFoundError('Accommodation', id)

        self.session.delete(db_accommodation)
        self.session.commit()