from typing import Optional, TypedDict


class BookingDTO(TypedDict):
    uuid: Optional[str]
    created_at: Optional[str]
    status: Optional[str]
    check_in: str
    check_out: str
    guest_name: str
    guest_phone: str
    accommodation_name: str
    accommodation_price: str
    total: str
    total_nights: str
