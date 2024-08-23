from pydantic import BaseModel


class Amenitie(BaseModel):
    id: int
    name: str


class AmenitieUpdateDTO(BaseModel):
    name: str | None


class AmenitieCreateDTO(BaseModel):
    name: str
