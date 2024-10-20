from pydantic import BaseModel
from ulid import ULID

from app.database.models import AccommodationDB, AccommodationStatus
from app.entities.Amenitie import Amenitie


class AccommodationUpdateDTO(BaseModel):
    name: str | None = None
    status: AccommodationStatus | None = None
    total_guests: int | None = None
    single_beds: int | None = None
    double_beds: int | None = None
    price: float | None = None
    amenities: list[str] | None = None


class AccommodationCreateDTO(BaseModel):
    name: str
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[str]


class Accommodation(BaseModel):
    ulid: ULID = ULID()
    name: str
    status: AccommodationStatus = AccommodationStatus.AVAIABLE
    total_guests: int
    single_beds: int
    double_beds: int
    price: float
    amenities: list[Amenitie] = []

    @classmethod
    def create(cls, dto: AccommodationCreateDTO):
        return cls(
            name=dto.name,
            total_guests=dto.total_guests,
            single_beds=dto.single_beds,
            double_beds=dto.double_beds,
            price=dto.price,
        )

    @classmethod
    def from_db(cls, db_accommodation: AccommodationDB):
        amenities = [
            Amenitie(name=amenitie.name)
            for amenitie in db_accommodation.amenities
        ]

        return cls(
            ulid=ULID.from_str(db_accommodation.ulid),
            name=db_accommodation.name,
            status=db_accommodation.status,
            total_guests=db_accommodation.total_guests,
            single_beds=db_accommodation.single_beds,
            double_beds=db_accommodation.double_beds,
            price=db_accommodation.price,
            amenities=amenities,
        )

    def add_amenitie(self, amenitie: Amenitie):
        self.amenities.append(amenitie)
