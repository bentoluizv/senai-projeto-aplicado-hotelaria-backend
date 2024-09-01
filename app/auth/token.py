from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from app.infra.database.db import get_database_session
from app.infra.database.models import UserDB
from app.schemas.Token import TokenData
from app.settings.Settings import Settings

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode,
        Settings().SECRET_KEY,  # type: ignore
        algorithm=Settings().ALGORITHM,  # type: ignore
    )
    return encoded_jwt


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
            key=Settings().SECRET_KEY,  # type: ignore
            algorithms=[Settings().ALGORITHM],  # type: ignore
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
