from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models import AccommodationDB
from app.domain.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.domain.errors.AlreadyExistsError import AlreadyExistsError
from app.domain.errors.NotFoundError import NotFoundError


class AccommodationRepository:
    def __init__(self, database: Session):
        self.database = database

    def list(self):
        db_accommodations = self.database.scalars(
            select(AccommodationDB)
        ).all()

        accommodation = [
            Accommodation.from_database(db_accommodation)
            for db_accommodation in db_accommodations
        ]

        return accommodation

    def find_by_id(self, id: int):
        db_accommodation = self.database.get(AccommodationDB, id)

        if not db_accommodation:
            raise NotFoundError(id)

        accommodation = Accommodation.from_database(db_accommodation)

        return accommodation

    def insert(self, data: AccommodationCreateDTO):
        accommodation = Accommodation.create(data)

        exists = self.database.scalar(
            select(AccommodationDB).where(
                AccommodationDB.name == accommodation.name
            )
        )

        if exists:
            raise AlreadyExistsError(accommodation.name)

        db_accommodation = AccommodationDB(**accommodation.model_dump())
        self.database.add(db_accommodation)
        self.database.commit()

    def update(self, data: AccommodationUpdateDTO):
        db_accommodation = self.database.get(AccommodationDB, id)

        if not db_accommodation:
            raise NotFoundError(id)

        for key, value in data.model_dump().items():
            if value is not None:
                setattr(db_accommodation, key, value)

        self.database.commit()

    def delete(self, id: int):
        db_accommodation = self.database.get(AccommodationDB, id)

        if not db_accommodation:
            raise NotFoundError(id)

        self.database.delete(db_accommodation)
