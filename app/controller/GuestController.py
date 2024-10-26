from typing import Annotated

from fastapi import Depends

from app.database.repositories.GuestRepository import GuestRepository
from app.entities.Guest import Guest, GuestCreateDTO, GuestUpdateDTO
from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.errors.OutOfRangeError import OutOfRangeError
from app.factory.RepositoryFactory import RepositoryFactory


class GuestController:
    guest_repository: GuestRepository

    def __init__(
        self,
        repository_factory: Annotated[
            RepositoryFactory, Depends(RepositoryFactory)
        ],
    ) -> None:
        self.guest_repository = repository_factory.create_guest_respository()

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Guest]:
        total_guests = self.guest_repository.count()

        if total_guests == 0:
            return []

        total_pages = (total_guests + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            raise OutOfRangeError(page, total_pages)

        guests = self.guest_repository.list_all(page, per_page)

        return guests

    def find_by_id(self, id: str):
        guest = self.guest_repository.find_by_id(id)

        if not guest:
            raise NotFoundError('Guest', id)

        return guest

    def create(self, dto: GuestCreateDTO):
        guest = self.guest_repository.find_by_document(dto.document)

        if guest:
            raise AlreadyExistsError('Guest', 'document', dto.document)

        guest = Guest.create(dto)

        self.guest_repository.create(guest)

    def update(self, id: str, dto: GuestUpdateDTO):
        existing = self.guest_repository.find_by_id(id)

        if not existing:
            raise NotFoundError('Guest', id)

        self.guest_repository.update(id, dto)

    def delete(self, id: str):
        existing = self.guest_repository.find_by_id(id)

        if not existing:
            raise NotFoundError('Guest', id)

        self.guest_repository.delete(id)
