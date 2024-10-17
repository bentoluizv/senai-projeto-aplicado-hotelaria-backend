from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import GuestDB, UserDB
from app.entities.User import User, UserCreateDTO


class UserRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        total_accommodation = self.session.scalar(
            select(func.count()).select_from(GuestDB)
        )

        return total_accommodation or 0

    def create(self, dto: UserCreateDTO) -> None:
        db_user = self.session.scalar(
            select(UserDB).where(UserDB.email == dto.email)
        )

        if db_user:
            return None

        user = User.create(dto)

        db_user = UserDB(
            ulid=str(user.ulid),
            email=user.email,
            password=user.password,
            role=user.role,
        )

        self.session.add(user)
        self.session.commit()

    def find_by_email(self, email: EmailStr) -> User | None:
        db_user = self.session.scalar(
            select(UserDB).where(UserDB.email == email)
        )

        if not db_user:
            return None

        user = User.from_db(db_user)

        return user
