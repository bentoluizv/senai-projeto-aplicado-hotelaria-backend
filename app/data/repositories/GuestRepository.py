from datetime import datetime
from typing import List

from click import echo

from app.data.dao.GuestDAO import GuestDAO
from app.entity.Guests import Guest


class GuestRepository:
    def __init__(self, dao: GuestDAO):
        self.dao = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, guest: Guest):
        exists = self.dao.findBy("document", guest.document)
        if exists:
            raise ValueError(f"Documento {guest.document} já está cadastrado")

        guest_dto = guest.to_dict()
        guest_dto["created_at"] = guest.formatted_created_at()  # Formatar data ao inserir
        self.dao.insert(guest_dto)

    def findBy(self, property: str, value: str):
        exists = self.dao.findBy(property, value)
        if not exists:
            raise ValueError(f"{property} -> {value} não está cadastrado")
        echo(exists)
        # Formatar string de volta para datetime ao buscar
        exists["created_at"] = datetime.fromisoformat(exists["created_at"])
        guest = Guest.from_dict(exists)
        return guest

    def find_many(self) -> List[Guest]:
        existing = self.dao.find_many()
        if len(existing) == 0:
            return []

        guests: List[Guest] = []
        for unknown in existing:
            # Formatar string de volta para datetime ao buscar
            unknown["created_at"] = datetime.fromisoformat(unknown["created_at"])
            guest = Guest.from_dict(unknown)
            guests.append(guest)
        return guests

    def update(self, guest: Guest):
        exists = self.dao.findBy("document", guest.document)
        if not exists:
            raise ValueError(f"Documento {guest.document} não está cadastrado")

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
            raise ValueError(f"Documento {document} não está cadastrado")
        self.dao.delete(document)
