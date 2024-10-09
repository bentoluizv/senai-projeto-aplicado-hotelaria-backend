from pydantic import BaseModel


class AmenitieUpdateDTO(BaseModel):
    name: str | None = None


class AmenitieCreateDTO(BaseModel):
    name: str


class Amenitie(BaseModel):
    name: str

    @classmethod
    def create(cls, dto: AmenitieCreateDTO):
        return cls(name=dto.name)
