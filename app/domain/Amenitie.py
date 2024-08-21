from typing import List

from pydantic import BaseModel


class Amenitie(BaseModel):
    id: int
    name: str


class AmenitieList(BaseModel):
    amenities: List[Amenitie]
