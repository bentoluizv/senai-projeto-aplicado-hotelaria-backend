from datetime import datetime

from pydantic import model_validator

from app.utils.StrictModel import StrictModel


class Accommodation(StrictModel):
    id: int
    created_at: datetime
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]

    @model_validator(mode='before')
    @classmethod
    def convert_str_to_crated_at_datetime(cls, data: dict):
        for k, v in data.items():
            if k in {'created_at'}:
                data[k] = datetime.fromisoformat(v)
        return data
