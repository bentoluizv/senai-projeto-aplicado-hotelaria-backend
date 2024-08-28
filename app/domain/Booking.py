from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from app.data.database.models import AccommodationDB, BookingDB, GuestDB
from app.domain.Accommodation import Accommodation
from app.domain.Guest import Guest
from app.utils.generate_locator import generate_locator


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


class BookingDTOWithGuestAndAccommodation(BookingCreateDTO):
    guest: Guest
    accommodation: Accommodation

    @model_validator(mode='before')
    @classmethod
    def check_input_data(cls, data: Any) -> Any:
        if data['accommodation_id'] != data['accommodation'].id:
            raise ValueError('Accommodation ID does not match')

        if data['guest_document'] != data['guest'].document:
            raise ValueError('Guest document does not match')

        return data


class Booking(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    locator: str = Field(default_factory=generate_locator)
    status: str
    check_in: datetime
    check_out: datetime
    guest: Guest
    accommodation: Accommodation
    budget: float

    @model_validator(mode='before')
    @classmethod
    def check_input_data(cls, data: Any) -> Any:
        if isinstance(data['accommodation'], AccommodationDB) and isinstance(
            data['guest'], GuestDB
        ):
            data['accommodation'] = Accommodation.from_database(
                data['accommodation']
            )

            data['guest'] = Guest.from_database(data['guest'])

        return data

    @classmethod
    def from_database(cls, data: BookingDB):
        return cls(**data.__dict__)

    @classmethod
    def create(cls, data: BookingDTOWithGuestAndAccommodation):
        return cls(**data.model_dump())
