from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.data.database.models import GuestDB


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
    document: str
    name: str
    surname: str
    phone: str
    country: str
    uuid: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_database(cls, data: GuestDB):
        return cls(**data.__dict__)

    @classmethod
    def create(cls, data: GuestCreateDTO):
        return cls(**data.model_dump())
