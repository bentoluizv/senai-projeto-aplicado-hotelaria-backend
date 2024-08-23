from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.Amenitie import Amenitie


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


class AccommodationCreateDTO(BaseModel):
    name: str
    status: str = 'Disponivel'
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]


class AccommodationUpdateDTO(BaseModel):
    name: str | None = None
    status: str | None = None
    total_guests: int | None = None
    single_beds: int | None = None
    double_beds: int | None = None
    min_nights: int | None = None
    price: int | None = None
    amenities: list[str] | None = None
