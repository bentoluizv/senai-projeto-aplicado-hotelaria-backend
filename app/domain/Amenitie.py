from typing import List

from pydantic import BaseModel, ConfigDict


class Amenitie(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    id: int
    name: str


class AmenitieList(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    amenities: List[Amenitie]
