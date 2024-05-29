from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Guest(BaseModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str
    created_at: datetime = Field(default=datetime.now())


    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()
