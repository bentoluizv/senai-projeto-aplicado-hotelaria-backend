from pydantic import BaseModel
from ulid import ULID


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
    ulid: ULID = ULID()
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
    def from_db(cls, db_guest):
        return cls(
            ulid=db_guest.ulid,
            document=db_guest.document,
            name=db_guest.name,
            surname=db_guest.surname,
            phone=db_guest.phone,
            country=db_guest.country,
        )

    def update(self, dto: GuestUpdateDTO):
        dto_as_dict = dto.model_dump()

        for field, value in dto_as_dict.items():
            if value is not None:
                setattr(self, field, value)
