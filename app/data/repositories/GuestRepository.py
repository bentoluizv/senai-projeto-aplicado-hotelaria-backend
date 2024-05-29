from typing import List
from app.data.dao.GuestDAO import GuestDAO
from app.entity.Guests import Guest


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao  = dao


    def count(self) -> int:
        return self.dao.count()


    def insert(self, guest: Guest):
        exists  = self.dao.find(guest.document)

        if exists:
            raise ValueError(f'Guest with document {guest.document} already exists')

        guest_dto = guest.to_dict()

        self.dao.insert(guest_dto)


    def find(self, document: str):
        exists = self.dao.find(document)

        if not exists:
            raise ValueError(f'Guest with document {document} not exists')

        guest = Guest.from_dict(exists)

        return guest


    def find_many(self) -> List[Guest]:
        existing = self.dao.find_many()

        if len(existing) == 0:
            return []

        guests: List[Guest] = []

        for unknown in existing:
            guest = Guest.from_dict(unknown)
            guests.append(guest)

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