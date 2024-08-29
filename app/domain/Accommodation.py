from datetime import datetime

from pydantic import BaseModel

from app.domain.Amenitie import Amenitie


class AccommodationUpdateDTO(BaseModel):
    name: str | None = None
    status: str | None = None
    total_guests: int | None = None
    single_beds: int | None = None
    double_beds: int | None = None
    price: float | None = None
    amenities: list[str] | None = None


class AccommodationCreateDTO(BaseModel):
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[str]


class Accommodation(BaseModel):
    id: int
    created_at: datetime
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[Amenitie]
