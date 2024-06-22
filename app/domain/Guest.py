from datetime import datetime
from typing import Any

from pydantic import model_validator

from app.utils.StrictModel import StrictModel


class Guest(StrictModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str
    created_at: datetime

    @model_validator(mode='before')
    @classmethod
    def parse_input_data(cls, data: dict[str, Any]):
        for k, v in data.items():
            if k in {'created_at'}:
                data[k] = datetime.fromisoformat(v)

        return data
