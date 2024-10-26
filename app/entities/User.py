from typing import Self

from pydantic import BaseModel, EmailStr, model_validator
from ulid import ULID

from app.auth.hash import generate_password_hash
from app.database.models import UserDB
from app.schemas.Enums import Role


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str
    password2: str
    role: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password2
        if pw1 != pw2:
            raise ValueError('passwords does not match')

        self.password = generate_password_hash(pw1)

        return self


class User(BaseModel):
    ulid: ULID | None = None
    email: EmailStr
    password: str
    role: Role

    @classmethod
    def create(cls, dto: UserCreateDTO):
        return cls(email=dto.email, password=dto.password, role=Role(dto.role))

    @classmethod
    def from_db(cls, db_user: UserDB):
        return cls(
            ulid=ULID.from_str(db_user.ulid),
            email=db_user.email,
            password=db_user.password,
            role=Role(db_user.role),
        )
