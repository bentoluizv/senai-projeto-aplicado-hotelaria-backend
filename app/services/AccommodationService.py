from http import HTTPStatus

from fastapi import HTTPException

from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.schemas.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)


class AccommodationService:
    accommodation_repository: AccommodationRepository

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.accommodation_repository = (
            repository_factory.create_accommodation_repository()
        )

    def create(self, dto: AccommodationCreateDTO):
        accommodation = self.accommodation_repository.find_by_name(dto.name)

        if accommodation:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Accommodation already exists',
            )
        accommodation = Accommodation.create(dto)

        self.accommodation_repository.create(accommodation)

    def delete(self, id: str):
        accommodation = self.accommodation_repository.find_by_id(id)

        if not accommodation:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

        self.accommodation_repository.delete(id)

    def find_by_id(self, id: str):
        accommodation = self.accommodation_repository.find_by_id(id)

        if not accommodation:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

        return accommodation

    def list_all(self, page: int, per_page: int):
        if page > self.accommodation_repository.info.total_pages:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='page out of range'
            )

        accommodations = self.accommodation_repository.list_all(page, per_page)

        return accommodations

    def update(self, id: str, dto: AccommodationUpdateDTO):
        accommodation = self.accommodation_repository.find_by_id(id)

        if not accommodation:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

        self.accommodation_repository.update(id, dto)
