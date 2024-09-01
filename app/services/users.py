from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.infra.database.models import UserDB
from app.schemas.User import UserCreateDTO


def create(session: Session, data: UserCreateDTO):
    existing_user = session.scalar(
        select(UserDB).where(UserDB.email == data.email)
    )
    if existing_user:
        raise AlreadyExistsError(data.email)

    user = UserDB(email=data.email, password=data.password, role=data.role)

    session.add(user)
    session.commit()
