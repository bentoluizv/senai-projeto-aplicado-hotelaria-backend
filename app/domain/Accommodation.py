from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.domain.Amenitie import Amenitie


class AccommodationDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(default='Disponivel')
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]


class Accommodation(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int | None
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
