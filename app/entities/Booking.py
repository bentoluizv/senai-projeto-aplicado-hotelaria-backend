from datetime import datetime
from typing import Self

from pydantic import (
    BaseModel,
    model_validator,
)
from ulid import ULID
from zoneinfo import ZoneInfo

from app.database.models import BookingDB
from app.entities.Accommodation import Accommodation
from app.entities.Guest import Guest
from app.entities.schemas.Enums import BookingStatus


class BookingUpdateDTO(BaseModel):
    status: str | None = None


class BookingCreateDTO(BaseModel):
    check_in: datetime
    check_out: datetime
    guest_document: str
    accommodation_ulid: str


class Booking(BaseModel):
    ulid: ULID | None = None
    locator: str | None = None
    status: BookingStatus = BookingStatus.PRE_RESERVA
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: float = 0

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

    @classmethod
    def from_db(cls, db_booking: BookingDB):
        return cls(
            ulid=ULID.from_str(db_booking.ulid),
            locator=db_booking.locator,
            check_in=db_booking.check_in,
            check_out=db_booking.check_out,
            guest=Guest.from_db(db_booking.guest),
            accommodation=Accommodation.from_db(db_booking.accommodation),
            status=BookingStatus(db_booking.status),
        )

    @model_validator(mode='after')
    def calculate_budget(self) -> Self:
        num_days = (self.check_out - self.check_in).days
        budget = num_days * self.accommodation.price
        self.budget = budget
        return self

    @model_validator(mode='after')
    def set_timezone(self) -> Self:
        self.check_in.replace(tzinfo=ZoneInfo('America/Sao_Paulo'))
        self.check_out.replace(tzinfo=ZoneInfo('America/Sao_Paulo'))
        return self

    def set_status(self, status: str):
        self.status = BookingStatus(status)
