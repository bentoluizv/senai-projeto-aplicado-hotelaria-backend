from datetime import datetime
from typing import TypedDict

#TODO: Implementar a validação dos dados de entrada da classe.

class AccommodationDTO(TypedDict):
    uuid: str
    name: str
    status: str
    total_guests: str
    single_beds: str
    double_beds: str
    min_nights: str
    price: str  
    created_at: str | None
     

class UpdatableAccommodation(TypedDict):   
    name: str
    status: str
    total_guests: str
    single_beds: str
    double_beds: str
    min_nights: str
    price: str  
    created_at: str | None

class Accommodation:
    def __init__(
            self,
            uuid: str,
            name: str,
            status: str,
            total_guests: str,
            single_beds: str,
            double_beds: str,
            min_nights: str,
            price: str,
            created_at: str | None = None):
        self.uuid = uuid
        self.name = name
        self.status = status
        self.total_guests = total_guests
        self.single_beds = single_beds
        self.single_beds = single_beds
        self.double_beds = double_beds
        self.min_nights = min_nights
        self.price = price
        self.created_at = datetime.fromisoformat(created_at) if created_at else datetime.now()

    @classmethod
    def from_dict(cls, accommodation_dto: AccommodationDTO):
        return cls(
            accommodation_dto['uuid'],
            accommodation_dto['name'],
            accommodation_dto['status'],
            accommodation_dto['total_guests'],
            accommodation_dto['single_beds'],
            accommodation_dto['double_beds'],
            accommodation_dto['min_nights'],          
            accommodation_dto['price'],
            accommodation_dto['created_at']
            
        )

    def to_dict(self) -> AccommodationDTO:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'status': self.status,
            'total_guests': self.total_guests,
            'single_beds': self.single_beds,
            'double_beds': self.double_beds,
            'min_nights': self.min_nights,
            'price': self.price,
            'created_at': self.created_at.isoformat()
        }
    
        