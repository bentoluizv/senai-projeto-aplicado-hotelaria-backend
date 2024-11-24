from typing import Annotated

from fastapi import Depends

from app.database.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.entities.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.entities.Amenitie import Amenitie
from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.errors.OutOfRangeError import OutOfRangeError
from app.factory.RepositoryFactory import RepositoryFactory


class AccommodationController:
    accommodation_repository: AccommodationRepository

    def __init__(
        self,
        repository_factory: Annotated[
            RepositoryFactory, Depends(RepositoryFactory)
        ],
    ) -> None:
        self.accommodation_repository = (
            repository_factory.create_accommodation_respository()
        )

    def list_all(
        self, page: int = 1, per_page: int = 10
    ) -> list[Accommodation]:
        total_accommodations = self.accommodation_repository.count()

        if total_accommodations == 0:
            return []

        total_pages = (total_accommodations + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            raise OutOfRangeError(page, total_pages)

        accommodations = self.accommodation_repository.list_all(page, per_page)

        return accommodations

    def find_by_id(self, id: str):
        accommodation = self.accommodation_repository.find_by_id(id)

        if not accommodation:
            raise NotFoundError('Accommodation', id)

        return accommodation

    def create(self, dto: AccommodationCreateDTO):
        accommodation = self.accommodation_repository.find_by_name(dto.name)

        if accommodation:
            raise AlreadyExistsError(
                'Accommodation',
                'name',
                dto.name,
            )

        accommodation = Accommodation.create(dto)

        self.accommodation_repository.create(accommodation)

    def update(self, ulid: str, dto: AccommodationUpdateDTO):
        accommodation = self.accommodation_repository.find_by_id(ulid)

        if not accommodation:
            raise NotFoundError('Accommodation', ulid)

        for field in dto.model_fields_set:
            if field != 'amenities':
                value = getattr(dto, field)
                if value is not None:
                    setattr(accommodation, field, value)

        if len(dto.amenities) == 0:
            accommodation.amenities = []
        else:
            accommodation.amenities = [
                Amenitie(name=amenitie) for amenitie in dto.amenities
            ]

        self.accommodation_repository.update(accommodation)

    def delete(self, id: str):
        accommodation = self.accommodation_repository.find_by_id(id)

        if not accommodation:
            raise NotFoundError('Accommodation', id)

        self.accommodation_repository.delete(id)
