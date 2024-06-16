from typing import Optional, TypedDict


class AccommodationModel(TypedDict):
    id: Optional[str]
    created_at: str
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int
    price: int
    amenities: list[str]
