from typing import List
from app.data.dao.GuestDAO import GuestDAO
from app.entity.Guests import Guest


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao  = dao


    def count(self) -> int:
        return self.dao.count()


    def insert(self, guest: Guest):
        exists  = self.dao.findBy('document',guest.document)

        if exists:
            raise ValueError(f'Documento {guest.document} já está cadastrado')

        guest_dto = guest.to_dict()

        self.dao.insert(guest_dto)


    def find(self, document: str):
        exists = self.dao.findBy('document',document)

        if not exists:
            raise ValueError(f'Documento {document} não está cadastrado')

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
        exists = self.dao.findBy('document',guest.document)

        if not exists:
            raise ValueError(f'Documento {guest.document} não está cadastrado')

        self.dao.update(
            guest.document,
            {
                'name': guest.name,
                'surname': guest.surname,
                'country': guest.country,
                'phone':   guest.phone
            })


    def delete(self, document: str):
        exists = self.dao.findBy('document',document)

        if not exists:
            raise ValueError(f'Documento {document} não está cadastrado')

        self.dao.delete(document)