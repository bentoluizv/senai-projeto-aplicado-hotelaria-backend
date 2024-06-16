from app.data.dao.GuestDAO import GuestDAO
from app.data.database.models.GuestModel import GuestModel
from app.entity.Guests import Guest
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, guest: Guest):
        exists = self.dao.findBy("document", guest.document)
        if exists:
            raise AlreadyExistsError()

        data = guest.to_dict()

        modelData: GuestModel = {
            "document": data["document"],
            "created_at": data["created_at"],
            "name": data["name"],
            "surname": data["surname"],
            "country": data["country"],
            "phone": data["phone"],
        }
        self.dao.insert(modelData)

    def findBy(self, property: str, value: str):
        exists = self.dao.findBy(property, value)

        if not exists:
            raise NotFoundError()

        guest = Guest.from_dict(exists)
        return guest

    def find_many(self) -> list[Guest]:
        existing = self.dao.find_many()
        if len(existing) == 0:
            return []

        guests: list[Guest] = []

        for unknown in existing:
            guest = Guest.from_dict(unknown)
            guests.append(guest)
        return guests

    def update(self, guest: Guest):
        exists = self.dao.findBy("document", guest.document)

        if not exists:
            raise NotFoundError()

        self.dao.update(
            guest.document,
            {
                "name": guest.name,
                "surname": guest.surname,
                "country": guest.country,
                "phone": guest.phone,
            },
        )

    def delete(self, document: str):
        exists = self.dao.findBy("document", document)
        if not exists:
            raise NotFoundError()
        self.dao.delete(document)
