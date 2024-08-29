from pydantic import BaseModel


class AmenitieUpdateDTO(BaseModel):
    name: str | None = None


class AmenitieCreateDTO(BaseModel):
    name: str


class Amenitie(BaseModel):
    id: int | None = None
    name: str
