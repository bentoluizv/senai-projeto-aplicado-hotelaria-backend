from pydantic import BaseModel
from ulid import ULID

from app.database.models import GuestDB


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
    ulid: ULID | None = None
    document: str
    name: str
    surname: str
    phone: str
    country: str

    @classmethod
    def create(cls, dto: GuestCreateDTO):
        return cls(
            document=dto.document,
            name=dto.name,
            surname=dto.surname,
            phone=dto.phone,
            country=dto.country,
        )

    @classmethod
    def from_db(cls, db_guest: GuestDB):
        return cls(
            ulid=ULID.from_str(db_guest.ulid),
            document=db_guest.document,
            name=db_guest.name,
            surname=db_guest.surname,
            phone=db_guest.phone,
            country=db_guest.country,
        )
