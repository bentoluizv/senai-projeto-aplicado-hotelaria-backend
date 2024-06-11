from datetime import datetime
from uuid import uuid4

from pydantic import (
    Field,
    field_validator,
    model_validator,
)

from app.entity.Accommodation import Accommodation
from app.entity.Guests import Guest
from app.utils.StrictModel import StrictModel


class Booking(StrictModel):
    uuid: str = Field(default=(str(uuid4())))
    created_at: str = Field(default=datetime.now().isoformat())
    status: str = Field(default="Aguardando Check-in")
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

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        expected_statuses = [
            "Aguardando Check-In",
            "Ativa",
            "Aguardando Check-Out",
            "Finalizada",
        ]
        if value not in expected_statuses:
            raise ValueError(
                f"Invalid status! [{value}] does not match any expected status: {expected_statuses}"
            )
        return value

    @model_validator(mode="after")
    def validate_check_in_check_out(self):
        if self.check_out < self.check_in:
            raise ValueError("Check out date is before check in")
        return self
