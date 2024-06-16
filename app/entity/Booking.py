from datetime import datetime
from uuid import uuid4

from app.entity.Accommodation import Accommodation
from app.entity.Guests import Guest
from app.utils.StrictModel import StrictModel
from pydantic import (
    Field,
    field_validator,
    model_validator,
)


class Booking(StrictModel):
    uuid: str = Field(default=(str(uuid4())))
    created_at: str = Field(default=datetime.now().isoformat())
    status: str = Field(default="Aguardando Check-In")
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

    def calculate_period(self):
        check_in = datetime.fromisoformat(self.check_in)
        check_out = datetime.fromisoformat(self.check_out)
        diffTime = check_out - check_in
        return diffTime.days

    def calculate_budget(self):
        price = self.accommodation.price
        period = self.calculate_period()

        return period * price

    def get_locator(self):
        locator = self.uuid[:6].replace("-", "")
        return locator
