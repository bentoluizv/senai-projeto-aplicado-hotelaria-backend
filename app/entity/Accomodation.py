from datetime import datetime
from typing import List, TypedDict, Union
from uuid import uuid4

#TODO: Implementar a validação dos dados de entrada da classe.

class AccommodationDTO(TypedDict):
    status: str
    name: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: List
    uuid: Union[str, None]
    created_at: Union[str, None]

class Accommodation:
    def __init__(self, accommodation_dto: AccommodationDTO):
        self.status: str = accommodation_dto.get('status')
        self.name: str= accommodation_dto.get('name')
        self.total_guests: int= accommodation_dto.get('total_guests')
        self.single_beds: int= accommodation_dto.get('single_beds')
        self.double_beds: int= accommodation_dto.get('double_beds')
        self.min_nights: int= accommodation_dto.get('min_nights')
        self.price: int= accommodation_dto.get('price')
        self.amenities: List = accommodation_dto.get('amenities')
        self.uuid: Union[str, None] = accommodation_dto.get('uuid')
        self.created_at: Union[str, None] = accommodation_dto.get('status')

        if(self.uuid is None):
            self.uuid = str(uuid4())

        if (self.created_at is None):
            self.created_at = datetime.now().isoformat()

        if (self.amenities is None):
            self.amenities = []

    def to_dict(self) -> AccommodationDTO:
        return {
            'status': self.status,
            'name': self.name,
            'total_guests': self.total_guests,
            'single_beds': self.single_beds,
            'double_beds': self.double_beds,
            'min_nights': self.min_nights,
            'price': self.price,
            'amenities': self.amenities,
            'uuid': self.uuid,
            'created_at': self.created_at
        }

    def add_amenitie(self, amenitie):
        self.amenities.append(amenitie)