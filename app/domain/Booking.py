from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.Accommodation import Accommodation
from app.domain.Guest import Guest


class BookingUpdateDTO(BaseModel):
    status: str | None = None
    check_in: datetime | None = None
    check_out: datetime | None = None
    guest_document: str | None = None
    accommodation_id: int | None = None
    budget: float | None = None


class BookingCreateDTO(BaseModel):
    status: str
    check_in: datetime
    check_out: datetime
    guest_document: str
    accommodation_id: int
    budget: float


class Booking(BaseModel):
    uuid: UUID
    created_at: datetime
    locator: str
    status: str
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: float
