from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.domain.Accommodation import Accommodation
from app.domain.Guest import Guest


class BookingDTO(BaseModel):
    locator: str
    status: str
    check_in: str
    check_out: str
    guest_document: str
    accommodation_id: int
    budget: int


class Booking(BaseModel):
    model_config = ConfigDict(frozen=True)

    uuid: str = Field(default=str(uuid4()))
    created_at: datetime = Field(default=datetime.now())
    locator: str
    status: str
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: int


class BookingList(BaseModel):
    bookings = List[Booking]
