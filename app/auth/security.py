from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.database.db import get_database_session
from app.database.models import UserDB
from app.entities.schemas.Token import TokenData
from app.settings.Settings import get_settings

settings = get_settings()


def get_current_user(
    session: Annotated[Session, Depends(get_database_session)],
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='auth'))],
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get('sub')

        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)

    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(UserDB).where(UserDB.email == token_data.email)
    )

    if not user:
        raise credentials_exception

    return user
