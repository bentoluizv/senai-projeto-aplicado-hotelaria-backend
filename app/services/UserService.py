from http import HTTPStatus

from fastapi import HTTPException

from app.factory.RepositoryFactory import RepositoryFactory
from app.infra.repositories.UserRepository import UserRepository
from app.schemas.User import UserCreateDTO


class UserService:
    user_repository: UserRepository

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.user_repository = repository_factory.create_user_repository()

    def create(self, dto: UserCreateDTO):
        user = self.user_repository.find_by_email(dto.email)

        if user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User already exists',
            )

        self.user_repository.create(dto)
