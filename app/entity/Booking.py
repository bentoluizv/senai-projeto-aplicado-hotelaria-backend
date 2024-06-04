from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field

from app.entity.Accommodation import Accommodation
from app.entity.Guests import Guest


class Booking(BaseModel):
    uuid: str = Field(default=str(uuid4()))
    created_at: str = Field(default=datetime.now().isoformat())
    status: str = Field(default='Aguardando Check-in')
    check_in: str
    check_out: str
    guest: Guest
    accommodation: Accommodation

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()