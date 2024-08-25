from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models import AmenitieDB
from app.domain.Amenitie import Amenitie, AmenitieCreateDTO, AmenitieUpdateDTO
from app.domain.errors.AlreadyExistsError import AlreadyExistsError
from app.domain.errors.NotFoundError import NotFoundError


class AmenitieRepository:
    def __init__(self, database: Session):
        self.database = database

    def list(self):
        db_amenities = self.database.scalars(select(AmenitieDB)).all()
        amenities = [
            Amenitie(id=db_amenitie.id, name=db_amenitie.name)
            for db_amenitie in db_amenities
        ]

        return amenities

    def find_by_id(self, id: int):
        db_amenitie = self.database.get(AmenitieDB, id)

        if not db_amenitie:
            raise NotFoundError(id)

        amenitie = Amenitie(id=db_amenitie.id, name=db_amenitie.name)
        return amenitie

    def insert(self, data: AmenitieCreateDTO):
        amenitie = Amenitie.create(data)
        exists = self.database.scalar(
            select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
        )

        if exists:
            raise AlreadyExistsError(amenitie.name)

        db_amenitie = AmenitieDB(amenitie.name)
        self.database.add(db_amenitie)
        self.database.commit()

    def update(self, id: int, data: AmenitieUpdateDTO):
        db_amenitie = self.database.get(AmenitieDB, id)

        if not db_amenitie:
            raise NotFoundError(id)

        for key, value in data.model_dump().items():
            if value is not None:
                setattr(db_amenitie, key, value)

        self.database.commit()

    def delete(self, id: int):
        db_amenitie = self.database.get(AmenitieDB, id)

        if not db_amenitie:
            raise NotFoundError(id)

        self.database.delete(db_amenitie)
