from pydantic import BaseModel


class AmenitieUpdateDTO(BaseModel):
    name: str | None = None


class AmenitieCreateDTO(BaseModel):
    name: str
