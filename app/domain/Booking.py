from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.Accommodation import Accommodation
from app.domain.Guest import Guest


class Booking(BaseModel):
    uuid: str = Field(default=str(uuid4()))
    created_at: datetime = Field(default=datetime.now())
    locator: str
    status: str
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: int

    def set_status(self, status: str):
        self.status = status

    def calculate_budget(self):
        period = self.check_out - self.check_in
        self.budget = period.days * self.accommodation.price


class BookingList(BaseModel):
    bookings: List[Booking]


class BookingUpdateDTO(BaseModel):
    status: str
    check_in: str
    check_out: str
    guest_document: str
    accommodation_id: int
    budget: int


class BookingCreationalDTO(BaseModel):
    status: str
    check_in: str
    check_out: str
    guest_document: str
    accommodation_id: int
    budget: int
