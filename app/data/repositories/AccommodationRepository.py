from typing import List

import click
from app.data.dao.AccommodationDAO import AccommodationDAO
from app.entity.Accommodation import Accommodation


class AccommodationtRepository:
    def __init__(self, dao: AccommodationDAO):
        self.dao  = dao


    def count(self) -> int:
        return self.dao.count()


    def insert(self, accommodation: Accommodation):
        exists  = self.dao.find('uuid', accommodation.uuid)

        if exists:
            raise ValueError(f'Accommodation with document {accommodation.uuid} already exists')

        self.dao.insert(accommodation.to_dict())


    def findBy(self, property: str, value: str):
        exists = self.dao.find(property, value)

        if not exists:
            raise ValueError(f'Accommodation with {property} {value} not exists')

        amenities = exists['amenities']
        exists['amenities'] = amenities.split(',')
        accommodation = Accommodation.from_dict(exists)
        return accommodation


    def find_many(self) -> List[Accommodation]:
        existing = self.dao.find_many()

        if len(existing) == 0:
            return []

        accommodations: List[Accommodation] = []

        for unknown in existing:
            amenities = unknown['amenities']
            unknown['amenities'] = amenities.split(',')
            accommodation = Accommodation.from_dict(unknown)
            accommodations.append(accommodation)

        return accommodations


    def update(self, accommodation: Accommodation):
        exists = self.dao.find('uuid', accommodation.uuid)

        if not exists:
            raise ValueError(f'Accommodation with document {accommodation.uuid} not exists')

        self.dao.update(
            str(accommodation.uuid),
            {
                'name': accommodation.name,
                'status': accommodation.status,
                'total_guests': accommodation.total_guests,
                'single_beds': accommodation.single_beds,
                'double_beds': accommodation.double_beds,
                'min_nights': accommodation.min_nights,
                'price': accommodation.price,
                'amenities': accommodation.amenities
            })


    def delete(self, uuid: str):
        exists = self.dao.find('uuid', uuid)

        if not exists:
            raise ValueError(f'Accommodation with document {uuid} not exists')

        self.dao.delete(uuid)