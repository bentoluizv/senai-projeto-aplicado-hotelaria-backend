from pydantic import BaseModel
from ulid import ULID

from app.schemas.Amenitie import Amenitie


class AccommodationUpdateDTO(BaseModel):
    name: str | None = None
    status: str | None = None
    total_guests: int | None = None
    single_beds: int | None = None
    double_beds: int | None = None
    price: float | None = None
    amenities: list[str] | None = None


class AccommodationCreateDTO(BaseModel):
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[str]


class Accommodation(BaseModel):
    ulid: ULID | None = None
    name: str
    status: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[Amenitie] = []

    @classmethod
    def create(cls, dto: AccommodationCreateDTO):
        return cls(
            name=dto.name,
            status=dto.status,
            total_guests=dto.total_guests,
            single_beds=dto.single_beds,
            double_beds=dto.double_beds,
            price=dto.price,
        )

    def add_amenitie(self, amenitie: Amenitie):
        self.amenities.append(amenitie)
