from typing import List
from app.data.dao.AccommodationDAO import AccommodationDAO
from app.entity.Accommodation import Accommodation


class AccommodationtRepository:
    def __init__(self, dao: AccommodationDAO):
        self.dao  = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, accommodation: Accommodation) -> None:
        exists  = self.dao.find(accommodation.document)

        if exists:
            raise ValueError(f'Accommodation with document {accommodation.document} already exists')

        self.dao.insert(accommodation.to_dict())

    def find(self, document: str) -> Accommodation:
        exists = self.dao.find(document)

        if not exists:
            raise ValueError(f'Accommodation with document {document} not exists')

        return Accommodation.from_dict(exists)

    def find_many(self) -> List[Accommodation]:
        existing_accommodations = self.dao.find_many()

        if len(existing_accommodations) == 0:
            return []

        accommodations = [ Accommodation.from_dict(accommodation) for accommodation in existing_accommodations]

        return accommodations

    def update(self, accommodation: Accommodation):
        exists = self.dao.find(accommodation.document)

        if not exists:
            raise ValueError(f'Accommodation with document {accommodation.document} not exists')

        self.dao.update(
            accommodation.document,
            {
            
                'uuid': accommodation.uuid,
                'name': accommodation.name,
                'status': accommodation.status,
                'total_guests': accommodation.total_guests,
                'single_beds': accommodation.single_beds,
                'double_beds': accommodation.double_beds,
                'min_nights': accommodation.min_nights,
                'price': accommodation.price,       

                
            })


    def delete(self, document: str):
        exists = self.dao.find(document)

        if not exists:
            raise ValueError(f'Accommodation with document {document} not exists')

        self.dao.delete(document)