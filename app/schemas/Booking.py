import enum
from datetime import datetime

from pydantic import BaseModel


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
    accommodation_id: int
