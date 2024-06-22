from datetime import date, datetime
from uuid import uuid4

from pydantic import (
    Field,
    model_validator,
)

from app.utils.StrictModel import StrictModel


class BookingCreationalSchema(StrictModel):
    locator: str
    status: str
    check_in: str
    check_out: str
    guest_document: str
    accommodation_id: int
    budget: int

    @model_validator(mode='before')
    @classmethod
    def convert_datetime_created_at_to_str(cls, data: dict):
        for k, v in data.items():
            if k in {'created_at'} and isinstance(v, datetime):
                data[k] = v.isoformat()
        return data

    @model_validator(mode='before')
    @classmethod
    def parse_str_values_to_int(cls, data: dict):
        for k, v in data.items():
            if k in {'accommodation_id', 'budget'}:
                data[k] = int(v)
        return data


class BookingDB(BookingCreationalSchema):
    uuid: str = Field(default=(str(uuid4())))
    created_at: str = Field(default=date.today().isoformat())
