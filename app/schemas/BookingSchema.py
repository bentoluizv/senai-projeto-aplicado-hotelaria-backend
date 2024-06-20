from datetime import date
from uuid import uuid4

from pydantic import (
    Field,
)

from app.utils.StrictModel import StrictModel


class BookingSchema(StrictModel):
    status: str
    check_in: str
    check_out: str
    guest_documemt: str
    accommodation_id: int
    budget: int


class BookingDB(BookingSchema):
    uuid: str = Field(default=(str(uuid4())))
    created_at: str = Field(default=date.today().isoformat())
