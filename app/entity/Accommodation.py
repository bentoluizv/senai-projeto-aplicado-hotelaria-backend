from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field



class Accommodation(BaseModel):
    uuid: str = Field(default=str(uuid4()))
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int = Field(default=2)
    price: int
    created_at: str = Field(default=datetime.now())


    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()
