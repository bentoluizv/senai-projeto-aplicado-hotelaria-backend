from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode='after')
    def update_status(self):
        today = datetime.now()
        is_in_check_in_period = today < self.check_in
        is_in_booking_period = (
            today > self.check_in and today <= self.check_out
        )
        is_in_check_out_period = today >= self.check_out

        if is_in_check_in_period:
            days_to_check_in = self.check_in - today
            if days_to_check_in.days <= 1:
                self.status = 'Aguardando Check In'
                self.accommodation.status = 'Aguardando Reserva'

        if is_in_booking_period:
            if self.status == 'Ativa':
                self.accommodation.status = 'Ocupada'

            if self.status != 'Ativa':
                self.status = 'Atrasada'

        if is_in_check_out_period:
            if self.status == 'Finalizada':
                self.accommodation.status = 'Disponivel'

            if self.status != 'Finalizada':
                if self.check_out == today:
                    self.status = 'Aguardando Checkout'

                if today > self.check_out:
                    self.status = 'Checkout Atrasado'

        return self

    def set_status(self, status: str):
        self.status = status

    def calculate_budget(self):
        period = self.check_out - self.check_in
        self.budget = period.days * self.accommodation.price


class BookingList(BaseModel):
    bookings: List[Booking]


class BookingUpdateDTO(BaseModel):
    status: str
    locator: str
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
