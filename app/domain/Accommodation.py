from datetime import datetime

from pydantic import BaseModel, Field

from app.data.database.models import AccommodationDB
from app.domain.Amenitie import Amenitie


class AccommodationUpdateDTO(BaseModel):
    name: str | None = None
    status: str | None = None
    total_guests: int | None = None
    single_beds: int | None = None
    double_beds: int | None = None
    min_nights: int | None = None
    price: float | None = None
    amenities: list[str] | None = None


class AccommodationCreateDTO(BaseModel):
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: float
    amenities: list[str]


class Accommodation(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=datetime.now)
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[Amenitie]

    @classmethod
    def from_database(cls, data: AccommodationDB):
        return cls(**data.__dict__)

    @classmethod
    def create(cls, data: AccommodationCreateDTO):
        return cls(**data.model_dump())
