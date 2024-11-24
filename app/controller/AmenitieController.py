from typing import Annotated

from fastapi import Depends

from app.database.repositories.AmenitieRepository import AmenitieRepository
from app.entities.Amenitie import Amenitie, AmenitieCreateDTO
from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.errors.OutOfRangeError import OutOfRangeError
from app.factory.RepositoryFactory import RepositoryFactory


class AmenitieController:
    amenitie_repository: AmenitieRepository

    def __init__(
        self,
        repository_factory: Annotated[
            RepositoryFactory, Depends(RepositoryFactory)
        ],
    ) -> None:
        self.amenitie_repository = (
            repository_factory.create_amenitie_respository()
        )

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Amenitie]:
        total_amenities = self.amenitie_repository.count()

        if total_amenities == 0:
            return []

        total_pages = (total_amenities + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            raise OutOfRangeError(page, total_pages)

        amenities = self.amenitie_repository.list_all(page, per_page)

        return amenities

    def find_by_name(self, name: str):
        amenitie = self.amenitie_repository.find_by_name(name)

        if not amenitie:
            raise NotFoundError('Amenitie', name)

        return amenitie

    def find_by_id(self, id: str):
        amenitie = self.amenitie_repository.find_by_id(id)

        if not amenitie:
            raise NotFoundError('Amenitie', id)

        return amenitie

    def create(self, dto: AmenitieCreateDTO):
        amenitie = self.amenitie_repository.find_by_name(dto.name)

        if amenitie:
            raise AlreadyExistsError('Amenitie', 'name', dto.name)

        amenitie = Amenitie.create(dto)

        self.amenitie_repository.create(amenitie)

    def delete(self, id: str):
        existing = self.amenitie_repository.find_by_id(id)

        if not existing:
            raise NotFoundError('Guest', id)

        self.amenitie_repository.delete(int(id))
