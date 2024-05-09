from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

#TODO: Implementar a validação dos dados de entrada da classe.

@dataclass
class Accommodation:
    def __init__(self, status: str, name: str, total_guests: int, single_beds: int, double_beds: int, min_nights: int, price: int,  uuid:str|None=None, created_at:str|None=None,):
        self.uuid = str(uuid4()) if uuid is None else uuid
        self.created_at = datetime.now().isoformat() if created_at is None else created_at
        self.status = status
        self.name = name
        self.total_guests = total_guests
        self.single_beds = single_beds
        self.double_beds = double_beds
        self.min_nights = min_nights
        self.price =  price
        self.amenities = []

    def toObj(self):
        return self.__dict__

    def add_amenitie(self, amenitie):
        self.amenities.append(amenitie)