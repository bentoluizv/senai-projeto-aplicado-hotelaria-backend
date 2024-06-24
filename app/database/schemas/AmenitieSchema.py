from pydantic import BaseModel


class Amenitie(BaseModel):
    name: str


class AmenitieDB(Amenitie):
    id: int
