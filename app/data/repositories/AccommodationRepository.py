from datetime import datetime
from typing import List
from uuid import UUID

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.entity.Accommodation import Accommodation


class AccommodationtRepository:
    def __init__(self, dao: AccommodationDAO):
        self.dao = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, accommodation: Accommodation):
        exists = self.dao.find("uuid", str(accommodation.uuid))

        if exists:
            raise ValueError(
                f"Accommodation with document {accommodation.uuid} already exists"
            )

        accommodation_dict = accommodation.to_dict()
        accommodation_dict["uuid"] = str(accommodation_dict["uuid"])
        accommodation_dict["created_at"] = accommodation_dict["created_at"].isoformat()

        self.dao.insert(accommodation_dict)

    def findBy(self, property: str, value: str):
        exists = self.dao.find(property, value)

        if not exists:
            raise ValueError(f"Accommodation with {property} {value} not exists")

        if exists["amenities"] is not None:
            amenities = exists["amenities"]
            exists["amenities"] = amenities.split(",")
        else:
            exists["amenities"] = []

        exists["uuid"] = UUID(exists["uuid"])
        exists["created_at"] = datetime.fromisoformat(exists["created_at"])
        accommodation = Accommodation.from_dict(exists)
        return accommodation

    def find_many(self):
        rawAccommodations = self.dao.find_many()
        if len(rawAccommodations) == 0:
            return []

        accommodations: List[Accommodation] = []

        for raw in rawAccommodations:
            if raw["amenities"] is not None:
                amenities = raw["amenities"]
                raw["amenities"] = amenities.split(",")
            else:
                raw["amenities"] = []

            raw["uuid"] = UUID(raw["uuid"])
            raw["created_at"] = datetime.fromisoformat(raw["created_at"])

            accommodation = Accommodation.from_dict(raw)
            accommodations.append(accommodation)

        return accommodations

    def update(self, accommodation: Accommodation):
        exists = self.dao.find("uuid", str(accommodation.uuid))

        if not exists:
            raise ValueError(
                f"Accommodation with document {accommodation.uuid} not exists"
            )

        self.dao.update(
            str(accommodation.uuid),
            {
                "name": accommodation.name,
                "status": accommodation.status,
                "total_guests": accommodation.total_guests,
                "single_beds": accommodation.single_beds,
                "double_beds": accommodation.double_beds,
                "min_nights": accommodation.min_nights,
                "price": accommodation.price,
                "amenities": accommodation.amenities,
            },
        )

    def delete(self, uuid: str):
        exists = self.dao.find("uuid", uuid)

        if not exists:
            raise ValueError(f"Accommodation with document {uuid} not exists")

        self.dao.delete(uuid)
