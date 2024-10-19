import pytest
from sqlalchemy import select

from app.database.models import UserDB
from app.entities.User import User, UserCreateDTO


@pytest.fixture()
def user_repository(repository_factory):
    user_repository = repository_factory.create_user_respository()
    return user_repository


def test_not_found_user_by_name(user_repository):
    existing = user_repository.find_by_email('user@user.com')
    assert not existing


def test_find_user_by_email(user_repository, db_user):
    user = user_repository.find_by_email('bentoluizv@gmail.com')
    assert user


def test_create_user(user_repository, session):
    dto = UserCreateDTO(
        email='bentoluizv@gmail.com',
        password='12334',
        password2='12334',
        role='admin',
    )
    user = User.create(dto)

    user_repository.create(user)

    user_created = session.scalar(
        select(UserDB).where(UserDB.email == user.email)
    )
    assert user_created is not None
    assert user.password.startswith('$argon2')
