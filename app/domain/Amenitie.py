from pydantic import BaseModel

from app.data.database.models import AmenitieDB


class AmenitieUpdateDTO(BaseModel):
    name: str | None = None


class AmenitieCreateDTO(BaseModel):
    name: str


class Amenitie(BaseModel):
    id: int
    name: str

    @classmethod
    def from_database(cls, data: AmenitieDB):
        return cls(**data.__dict__)

    @classmethod
    def create(cls, data: AmenitieCreateDTO):
        return cls(**data.model_dump())
