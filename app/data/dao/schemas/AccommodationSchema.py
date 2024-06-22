from datetime import datetime

from pydantic import (
    Field,
    model_validator,
)

from app.utils.StrictModel import StrictModel


class AccommodationCreationalSchema(StrictModel):
    created_at: str = Field(default=datetime.now().isoformat())
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int = Field(default=2)
    price: int
    amenities: list[str]

    @model_validator(mode='before')
    @classmethod
    def convert_datetime_created_at_to_str(cls, data: dict):
        for k, v in data.items():
            if k in {'created_at'} and isinstance(v, datetime):
                data[k] = v.isoformat()
        return data


class AccommodationDB(AccommodationCreationalSchema):
    id: int
