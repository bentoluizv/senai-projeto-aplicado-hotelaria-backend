from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GuestUpdateDTO(BaseModel):
    document: str | None = None
    name: str | None = None
    surname: str | None = None
    phone: str | None = None
    country: str | None = None


class GuestCreateDTO(BaseModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str


class Guest(BaseModel):
    uuid: UUID
    created_at: datetime
    document: str
    name: str
    surname: str
    phone: str
    country: str
