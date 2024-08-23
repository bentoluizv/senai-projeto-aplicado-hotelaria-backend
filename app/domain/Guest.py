from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Guest(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default=datetime.now())
    document: str
    name: str
    surname: str
    phone: str
    country: str


class GuestUpdatetableDTO(BaseModel):
    document: str | None
    name: str | None
    surname: str | None
    phone: str | None
    country: str | None


class GuestCreateDTO(BaseModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str
