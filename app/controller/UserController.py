from typing import Annotated

from fastapi import Depends

from app.database.repositories.UserRepository import UserRepository
from app.entities.User import User, UserCreateDTO
from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.factory.RepositoryFactory import RepositoryFactory


class UserController:
    user_repository: UserRepository

    def __init__(
        self,
        repository_factory: Annotated[
            RepositoryFactory, Depends(RepositoryFactory)
        ],
    ) -> None:
        self.user_repository = repository_factory.create_user_respository()

    def find_by_email(self, email: str):
        user = self.user_repository.find_by_email(email)

        if not user:
            raise NotFoundError('User', email)

        return user

    def find_by_id(self, id: str):
        user = self.user_repository.find_by_id(id)

        if not user:
            raise NotFoundError('User', id)

        return user

    def create(self, dto: UserCreateDTO):
        user = self.user_repository.find_by_email(dto.email)

        if user:
            raise AlreadyExistsError('User', 'email', dto.email)

        user = User.create(dto)

        self.user_repository.create(user)
