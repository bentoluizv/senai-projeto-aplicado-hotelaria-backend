from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field



class Accommodation(BaseModel):
    uuid: str = Field(default=str(uuid4()))
    name: str
    status: str = Field(default="Dísponivel")
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int = Field(default=2)
    price: int
    created_at: str = Field(default=datetime.now().isoformat())
    amenities: List[str] = Field(default=[])


    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()
