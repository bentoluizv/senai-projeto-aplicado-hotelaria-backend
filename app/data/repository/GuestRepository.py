from typing import Any

from app.data.dao.GuestDAO import GuestDAO
from app.data.dao.schemas.GuestSchema import GuestCreationalSchema
from app.domain.Guest import Guest
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao = dao

    def find_many(self) -> list[Guest]:
        guests_db = self.dao.find_many()

        return [Guest(**guest_db.model_dump()) for guest_db in guests_db]

    def find(self, id: str) -> Guest:
        guest_db = self.dao.find(id)

        if not guest_db:
            raise NotFoundError()

        return Guest(**guest_db.model_dump())

    def find_by(self, property: str, value: str) -> list[Guest]:
        guests_db = self.dao.find_by(property, value)

        if not guests_db:
            return []

        return [Guest(**guest_db.model_dump()) for guest_db in guests_db]

    def create(self, data: dict[str, Any]):
        guest = GuestCreationalSchema(**data)
        exists = self.dao.find(guest.document)

        if exists:
            raise AlreadyExistsError()

        self.dao.create(guest)

    def update(self, data: dict[str, Any]):
        guest_data = GuestCreationalSchema(**data)
        exists = self.dao.find(guest_data.document)

        if not exists:
            raise NotFoundError()

        self.dao.update(guest_data)

    def delete(self, document: str):
        exists = self.dao.find(document)

        if not exists:
            raise NotFoundError()

        self.dao.delete(document)
