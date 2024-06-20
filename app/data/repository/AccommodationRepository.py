from app.data.dao.AccommodationDAO import AccommodationDAO
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.schemas.AccommodationSchema import (
    AccommodationDB,
    AccommodationSchema,
)


class AccommodationRepository:
    def __init__(self, dao: AccommodationDAO):
        self.dao = dao

    def find_many(self) -> list[AccommodationDB]:
        return self.dao.find_many()

    def find(self, id: str) -> AccommodationDB:
        guest = self.dao.find(id)

        if not guest:
            raise NotFoundError()

        return guest

    def findBy(self, property: str, value: str) -> list[AccommodationDB]:
        guest = self.dao.find_by(property, value)

        if not guest:
            raise NotFoundError()

        return guest

    def create(self, accommodation: AccommodationSchema):
        guest = self.dao.find_by('name', accommodation.name)

        if guest:
            raise AlreadyExistsError()

        self.dao.create(accommodation)

    def update(self, accommodation: AccommodationSchema):
        exists = self.dao.find_by('name', accommodation.name)

        if not exists:
            raise NotFoundError()

        self.dao.update(str(exists[0].id), accommodation)

    def delete(self, id: str):
        exists = self.dao.find(id)

        if not exists:
            raise NotFoundError()

        self.dao.delete(id)
