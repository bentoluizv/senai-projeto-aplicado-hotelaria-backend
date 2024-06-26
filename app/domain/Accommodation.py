from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.domain.Amenitie import Amenitie


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
