from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import UserDB
from app.entities.User import User


class UserRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        total_accommodation = self.session.scalar(
            select(func.count()).select_from(UserDB)
        )

        return total_accommodation or 0

    def create(self, user: User) -> None:
        db_user = UserDB(
            ulid=str(user.ulid),
            email=user.email,
            password=user.password,
            role=user.role,
        )

        self.session.add(db_user)
        self.session.commit()

    def find_by_email(self, email: EmailStr) -> User | None:
        db_user = self.session.scalar(
            select(UserDB).where(UserDB.email == email)
        )

        if not db_user:
            return None

        user = User.from_db(db_user)

        return user

    def find_by_id(self, id: str) -> User | None:
        db_user = self.session.scalar(select(UserDB).where(UserDB.ulid == id))

        if not db_user:
            return None

        user = User.from_db(db_user)

        return user
