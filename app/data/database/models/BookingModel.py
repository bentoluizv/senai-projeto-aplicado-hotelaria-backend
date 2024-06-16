from typing import Optional, TypedDict

from app.data.database.models.AccommodationModel import AccommodationModel
from app.data.database.models.GuestModel import GuestModel


class BookingModel(TypedDict):
    uuid: Optional[str]
    created_at: str
    status: str
    check_in: str
    check_out: str
    guest: GuestModel
    accommodation: AccommodationModel
