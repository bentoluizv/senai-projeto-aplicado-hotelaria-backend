from typing import List
from app.data.dao.GuestDAO import GuestDAO
from app.entity.Guests import Guest


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao  = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, guest: Guest) -> None:
        exists  = self.dao.find(guest.document)

        if exists:
            raise ValueError(f'Guest with document {guest.document} already exists')

        self.dao.insert(guest.to_dict())

    def find(self, document: str) -> Guest:
        exists = self.dao.find(document)

        if not exists:
            raise ValueError(f'Guest with document {document} not exists')

        return Guest.from_dict(exists)

    def find_many(self) -> List[Guest]:
        existing_guests = self.dao.find_many()

        if len(existing_guests) == 0:
            return []

        guests = [ Guest.from_dict(guest) for guest in existing_guests]

        return guests

    def update(self, guest: Guest):
        exists = self.dao.find(guest.document)

        if not exists:
            raise ValueError(f'Guest with document {guest.document} not exists')

        self.dao.update(
            guest.document,
            {
                'name': guest.name,
                'surname': guest.surname,
                'country': guest.country,
                'phone':   guest.phone
            })


    def delete(self, document: str):
        exists = self.dao.find(document)

        if not exists:
            raise ValueError(f'Guest with document {document} not exists')

        self.dao.delete(document)