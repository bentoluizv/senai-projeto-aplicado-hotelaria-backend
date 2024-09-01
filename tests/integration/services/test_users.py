from sqlalchemy import select

from app.infra.database.models import UserDB
from app.schemas.User import Role, UserCreateDTO
from app.services.users import create


def test_create_new_user(session):
    data = UserCreateDTO(
        email='teste2@teste.com',
        password='123456',
        password2='123456',
        role=Role.ADMIN,
    )
    create(session, data)

    user = session.scalar(select(UserDB).where(UserDB.email == data.email))

    assert user.email == data.email
    assert user.password.startswith('$argon')
