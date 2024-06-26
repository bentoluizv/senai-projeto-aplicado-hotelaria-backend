from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Guest(BaseModel):
    model_config = ConfigDict(frozen=True)

    created_at: datetime = Field(default=datetime.now())
    document: str
    name: str
    surname: str
    phone: str
    country: str


class GuestList(BaseModel):
    guests: List[Guest]
