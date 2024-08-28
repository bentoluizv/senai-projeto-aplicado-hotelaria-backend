from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from app.data.database.models import AccommodationDB, AmenitieDB
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
    id: int | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[Amenitie]

    @model_validator(mode='before')
    @classmethod
    def check_input_data(cls, data: Any) -> Any:
        if all(isinstance(item, str) for item in data['amenities']):
            data['amenities'] = [
                Amenitie(name=amenitie) for amenitie in data['amenities']
            ]

        if all(isinstance(item, AmenitieDB) for item in data['amenities']):
            data['amenities'] = [
                Amenitie(name=amenitie.name, id=amenitie.id)
                for amenitie in data['amenities']
            ]
        return data

    @classmethod
    def from_database(cls, data: AccommodationDB):
        return cls(**data.__dict__)

    @classmethod
    def create(cls, data: AccommodationCreateDTO):
        return cls(**data.model_dump())
