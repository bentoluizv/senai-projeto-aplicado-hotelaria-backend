from app.database.schemas.AccommodationSchema import (
    AccommodationCreationalSchema,
    AccommodationDB,
)
from app.database.sqlite.dao.AccommodationDAO import AccommodationDAO
from app.domain.Accommodation import Accommodation
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class AccommodationRepository:
    def __init__(self, dao: AccommodationDAO):
        self.dao = dao

    def find_many(self) -> list[Accommodation]:
        accommodations_db = self.dao.find_many()

        return [
            Accommodation(**accommodation_db.model_dump())
            for accommodation_db in accommodations_db
        ]

    def find(self, id: int) -> Accommodation:
        exists = self.dao.find(id)

        if not exists:
            raise NotFoundError()

        return Accommodation(**exists.model_dump())

    def find_by(self, property: str, value: str) -> list[Accommodation]:
        exists = self.dao.find_by(property, value)

        if not exists:
            return []

        return [
            Accommodation(**accommodation_db.model_dump())
            for accommodation_db in exists
        ]

    def create(self, accommodation: AccommodationCreationalSchema):
        exists = self.dao.find_by('name', accommodation.name)

        if exists:
            raise AlreadyExistsError()

        self.dao.create(accommodation)

    def update(self, accommodation: Accommodation):
        exists = self.dao.find(accommodation.id)

        if not exists:
            raise NotFoundError()
        self.dao.update(AccommodationDB(**accommodation.model_dump()))

    def delete(self, id: int):
        exists = self.dao.find(id)

        if not exists:
            raise NotFoundError()

        self.dao.delete(id)
