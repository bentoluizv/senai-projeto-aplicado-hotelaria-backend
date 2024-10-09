import enum
from datetime import datetime

from pydantic import BaseModel
from ulid import ULID

from app.schemas.Accommodation import Accommodation
from app.schemas.Guest import Guest


class Status(enum.Enum):
    BOOKED = 'booked'
    WAITING_CHECK_IN = 'waiting check in'
    ACTIVE = 'active'
    WAITING_CHECK_OUT = 'waiting check out'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class BookingUpdateDTO(BaseModel):
    status: Status | None = None
    check_in: datetime | None = None
    check_out: datetime | None = None
    budget: float | None = None


class BookingCreateDTO(BaseModel):
    check_in: datetime
    check_out: datetime
    guest_document: str
    accommodation_ulid: str


class Booking(BaseModel):
    ulid: ULID | None = None
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
            check_in=dto.check_in,
            check_out=dto.check_out,
            guest=guest,
            accommodation=accommodation,
        )

    def calculate_budget(self):
        num_days = (self.check_out - self.check_in).days
        budget = num_days * self.accommodation.price

        return budget
