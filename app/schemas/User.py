import enum
from typing import Self

from pydantic import BaseModel, EmailStr, model_validator

from app.auth.hash import generate_password_hash


class Role(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str
    password2: str
    role: Role

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password2
        if (pw1 is not None) and (pw2 is not None) and (pw1 != pw2):
            raise ValueError('passwords does not match')

        self.password = generate_password_hash(pw1)

        return self


class User(BaseModel):
    email: EmailStr
    password: str
    role: Role

    @classmethod
    def create(cls, dto: UserCreateDTO):
        return cls(email=dto.email, password=dto.password, role=dto.role)
