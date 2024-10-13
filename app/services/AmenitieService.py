from http import HTTPStatus

from fastapi import HTTPException

from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.repositories.AmenitieRepository import AmenitieRepository
from app.schemas.Amenitie import Amenitie, AmenitieCreateDTO


class AmenitieService:
    amenitie_repository: AmenitieRepository

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.amenitie_repository = (
            repository_factory.create_amenitie_repository()
        )

    def create(self, dto: AmenitieCreateDTO):
        amenitie = self.amenitie_repository.find_by_name(dto.name)

        if amenitie:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Accommodation already exists',
            )

        amenitie = Amenitie.create(dto)

        self.amenitie_repository.create(amenitie)

    def list_all(self, page: int, per_page: int):
        if page > self.amenitie_repository.info.total_pages:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='page out of range'
            )

        amenities = self.amenitie_repository.list_all(page, per_page)

        return amenities

    def find_by_name(self, name: str):
        amenitie = self.amenitie_repository.find_by_name(name)

        if not amenitie:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

        return amenitie
