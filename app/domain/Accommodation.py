from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.domain.Amenitie import Amenitie


class AccommodationCreationalDTO(BaseModel):
    name: str
    status: str = Field(default='Disponivel')
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]


class AccommodationUpdateDTO(BaseModel):
    id: int
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]


class Accommodation(BaseModel):
    id: int
    created_at: datetime = Field(default=datetime.now())
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[Amenitie]


class AccommodationList(BaseModel):
    accommodations: List[Accommodation]
