import enum
from datetime import datetime
from typing import Self

from pydantic import BaseModel, model_validator
from ulid import ULID

from app.database.models import BookingDB
from app.entities.Accommodation import Accommodation
from app.entities.Guest import Guest


class Status(enum.Enum):
    BOOKED = 'booked'
    WAITING_CHECK_IN = 'waiting check in'
    ACTIVE = 'active'
    WAITING_CHECK_OUT = 'waiting check out'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class BookingUpdateDTO(BaseModel):
    check_in: datetime | None = None
    check_out: datetime | None = None
    budget: float | None = None


class BookingCreateDTO(BaseModel):
    check_in: datetime
    check_out: datetime
    guest_document: str
    accommodation_ulid: str


class Booking(BaseModel):
    ulid: ULID = ULID()
    status: Status = Status.BOOKED
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: float | None = None

    @classmethod
    def create(
        cls,
        dto: BookingCreateDTO,
        guest: Guest,
        accommodation: Accommodation,
    ):
        if (
            accommodation.ulid != dto.accommodation_ulid
            or guest.document != dto.guest_document
        ):
            raise ValueError('guest/accommodation is diff from dto')

        return cls(
            ulid=ULID(),
            check_in=dto.check_in,
            check_out=dto.check_out,
            guest=guest,
            accommodation=accommodation,
        )

    @classmethod
    def from_db(cls, db_booking: BookingDB):
        return cls(
            ulid=ULID.from_str(db_booking.ulid),
            check_in=db_booking.check_in,
            check_out=db_booking.check_out,
            guest=Guest.from_db(db_booking.guest),
            accommodation=Accommodation.from_db(db_booking.accommodation),
        )

    @model_validator(mode='after')
    def calculate_budget(self) -> Self:
        num_days = (self.check_out - self.check_in).days
        budget = num_days * self.accommodation.price
        self.budget = budget
        return self
