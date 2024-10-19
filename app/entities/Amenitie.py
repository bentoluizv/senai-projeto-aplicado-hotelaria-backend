from pydantic import BaseModel

from app.database.models import AmenitieDB


class AmenitieUpdateDTO(BaseModel):
    name: str | None = None


class AmenitieCreateDTO(BaseModel):
    name: str


class Amenitie(BaseModel):
    id: int | None = None
    name: str

    @classmethod
    def create(cls, dto: AmenitieCreateDTO):
        return cls(name=dto.name)

    @classmethod
    def from_db(cls, db_amenitie: AmenitieDB):
        return cls(id=db_amenitie.id, name=db_amenitie.name)
