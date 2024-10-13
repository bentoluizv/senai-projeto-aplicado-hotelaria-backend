from http import HTTPStatus

from fastapi import HTTPException

from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.repositories.GuestRepository import GuestRepository
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO


class GuestService:
    guest_repository: GuestRepository

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.guest_repository = repository_factory.create_guest_repository()

    def create(self, dto: GuestCreateDTO):
        guest = self.guest_repository.find_by_document(dto.document)

        if guest:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Guest Already Exists',
            )

        self.guest_repository.create(dto)

    def find_by_id(self, id: str):
        guest = self.guest_repository.find_by_id(id)

        if not guest:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Guest not found',
            )

        return guest

    def list_all(self, page: int = 1, per_page: int = 10):
        if page > self.guest_repository.info.total_pages:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='page out of range'
            )

        guests = self.guest_repository.list_all(page, per_page)

        return guests

    def update(self, id: str, dto: GuestUpdateDTO):
        guest = self.guest_repository.find_by_id(id)

        if not guest:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Guest not found',
            )

        self.guest_repository.update(id, dto)

    def delete(self, id: str):
        guest = self.guest_repository.find_by_id(id)

        if not guest:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Guest not found',
            )

        self.guest_repository.delete(id)
