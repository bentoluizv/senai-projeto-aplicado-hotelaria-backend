from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.models.AccommodationModel import AccommodationModel
from app.entity.Accommodation import Accommodation
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class AccommodationtRepository:
    def __init__(self, dao: AccommodationDAO):
        self.dao = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, accommodation: Accommodation):
        exists = self.dao.findBy("name", accommodation.name)

        if exists:
            raise AlreadyExistsError()

        accommodation_dict = accommodation.to_dict()

        modelData: AccommodationModel = {
            "id": accommodation_dict["id"],
            "name": accommodation_dict["name"],
            "created_at": accommodation_dict["created_at"],
            "status": accommodation_dict["status"],
            "total_guests": accommodation_dict["total_guests"],
            "single_beds": accommodation_dict["single_beds"],
            "double_beds": accommodation_dict["double_beds"],
            "min_nights": accommodation_dict["min_nights"],
            "price": accommodation_dict["price"],
            "amenities": accommodation_dict["amenities"],
        }
        self.dao.insert(modelData)

    def findBy(self, property: str, value: str) -> Accommodation:
        exists = self.dao.findBy(property, value)

        if not exists:
            raise NotFoundError()

        accommodation = Accommodation.from_dict(exists)
        return accommodation

    def find_many(self) -> list[Accommodation]:
        data = self.dao.find_many()
        accommodations: list[Accommodation] = []

        if len(data) == 0:
            return accommodations

        for accommodation_data in data:
            accommodation = Accommodation.from_dict(accommodation_data)
            accommodations.append(accommodation)

        return accommodations

    def update(self, accommodation: Accommodation):
        if not accommodation.id:
            raise ValueError()
        exists = self.dao.findBy("id", str(accommodation.id))

        if not exists:
            raise NotFoundError()

        self.dao.update(
            str(accommodation.id),
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

    def delete(self, id: str):
        exists = self.dao.findBy("id", id)

        if not exists:
            raise NotFoundError()

        self.dao.delete(id)
