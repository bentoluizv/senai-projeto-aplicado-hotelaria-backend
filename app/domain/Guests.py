from dataclasses import dataclass
from datetime import datetime
from typing import List, TypedDict, Union

#TODO: Implementar a validação dos dados de entrada da classe.

class GuestDTO(TypedDict):
    document: str
    name: str
    surname: str
    country: str
    phone: str
    created_at: str | None

class Guest:
    def __init__(self, guest_dto: GuestDTO):
        self.document = guest_dto.get('document')
        self.name = guest_dto.get('name')
        self.surname = guest_dto.get('surname')
        self.phone = guest_dto.get('phone')
        self.country = guest_dto.get('country')
        self.created_at = guest_dto.get('created_at')

        if(self.created_at is None):
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> GuestDTO:
        return {
            'document': self.document,
            'name': self.name,
            'surname': self.surname,
            'phone': self.phone,
            'country': self.country,
            'created_at': self.created_at
        }