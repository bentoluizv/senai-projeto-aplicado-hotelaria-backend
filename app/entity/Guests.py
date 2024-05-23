from datetime import datetime
from typing import TypedDict

#TODO: Implementar a validação dos dados de entrada da classe.

class GuestDTO(TypedDict):
    document: str
    name: str
    surname: str
    country: str
    phone: str
    created_at: str | None

class UpdatableGuest(TypedDict):
    name: str
    surname: str
    country: str
    phone: str

class Guest:
    def __init__(
            self,
            document: str,
            name: str,
            surname: str,
            phone: str,
            country: str,
            created_at: str | None = None):
        self.document = document
        self.name = name
        self.surname = surname
        self.phone = phone
        self.country = country
        self.created_at = datetime.fromisoformat(created_at) if created_at else datetime.now()

    @classmethod
    def from_dict(cls, guest_dto: GuestDTO):
        return cls(
            guest_dto['document'],
            guest_dto['name'],
            guest_dto['surname'],
            guest_dto['phone'],
            guest_dto['country'],
            guest_dto['created_at']
        )

    def to_dict(self) -> GuestDTO:
        return {
            'document': self.document,
            'name': self.name,
            'surname': self.surname,
            'phone': self.phone,
            'country': self.country,
            'created_at': self.created_at.isoformat()
        }