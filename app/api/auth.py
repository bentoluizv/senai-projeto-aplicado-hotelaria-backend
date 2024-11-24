from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.hash import verify_password
from app.auth.security import get_current_user
from app.auth.token import create_access_token
from app.database.db import get_database_session
from app.database.models import UserDB
from app.entities.schemas.Token import Token
from app.entities.User import PublicUser

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_database_session)]
CurrentUser = Annotated[UserDB, Depends(get_current_user)]


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):  # type: ignore
    user = session.scalar(
        select(UserDB).where(UserDB.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'bearer'}


@router.get('/current', response_model=PublicUser)
def return_current_user(
    user: CurrentUser,
):
    return user
