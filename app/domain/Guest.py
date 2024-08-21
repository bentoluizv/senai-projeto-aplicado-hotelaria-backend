from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Guest(BaseModel):
    created_at: datetime = Field(default=datetime.now())
    document: str
    name: str
    surname: str
    phone: str
    country: str


class GuestList(BaseModel):
    guests: List[Guest]
