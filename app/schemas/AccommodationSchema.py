from datetime import datetime

from pydantic import (
    Field,
)

from app.utils.StrictModel import StrictModel


class AccommodationSchema(StrictModel):
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]


class AccommodationDB(AccommodationSchema):
    id: int
    created_at: str = Field(default=datetime.now().isoformat())
