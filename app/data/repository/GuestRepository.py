from app.data.dao.GuestDAO import GuestDAO
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.schemas.GuestSchema import GuestDB, GuestSchema


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao = dao

    def find_many(self) -> list[GuestDB]:
        return self.dao.find_many()

    def find(self, id: str) -> GuestDB:
        guest = self.dao.find(id)

        if not guest:
            raise NotFoundError()

        return guest

    def findBy(self, property: str, value: str) -> list[GuestDB]:
        guest = self.dao.find_by(property, value)

        if not guest:
            raise NotFoundError()

        return guest

    def create(self, guest: GuestSchema):
        exists = self.dao.find(guest.document)

        if exists:
            raise AlreadyExistsError()

        self.dao.create(guest)

    def update(self, guest: GuestSchema):
        exists = self.dao.find(guest.document)

        if not exists:
            raise NotFoundError()

        self.dao.update(guest.document, guest)

    def delete(self, document: str):
        exists = self.dao.find(document)

        if not exists:
            raise NotFoundError()

        self.dao.delete(document)
