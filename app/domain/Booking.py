from datetime import datetime

from pydantic import model_validator

from app.domain.Accommodation import Accommodation
from app.domain.Guest import Guest
from app.utils.StrictModel import StrictModel


class Booking(StrictModel):
    uuid: str
    created_at: datetime
    locator: str
    status: str
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: int

    @model_validator(mode='before')
    @classmethod
    def convert_str_to_crated_at_datetime(cls, data: dict):
        for k, v in data.items():
            if k in {'created_at', 'check_in', 'check_out'}:
                data[k] = datetime.fromisoformat(v)

        return data

    @model_validator(mode='after')
    def check_check_in_check_out_rules(self):
        MINIMUM_STAY = 2

        check_in = self.check_in
        check_out = self.check_out

        if check_out < check_in:
            raise ValueError('Error: Check-out must be after Check-in')

        date_diff = check_out - check_in

        if date_diff.days < MINIMUM_STAY:
            raise ValueError(
                'Error: The smallest number of days allowed is two'
            )

        return self
