from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.Accommodation import Accommodation
from app.domain.Guest import Guest


class Booking(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default=datetime.now())
    locator: str
    status: str
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: int


class BookingUpdateDTO(BaseModel):
    status: str | None
    check_in: str | None
    check_out: str | None
    guest_document: str | None
    accommodation_id: int | None
    budget: int | None


class BookingCreateDTO(BaseModel):
    status: str
    check_in: str
    check_out: str
    guest_document: str
    accommodation_id: int
    budget: int
