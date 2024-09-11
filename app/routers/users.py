from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.infra.database.db import get_database_session
from app.schemas.Message import Message
from app.schemas.User import UserCreateDTO
from app.services.users import (
    create,
)

router = APIRouter(tags=['Users'], prefix='/users')


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_users(
    new_user: UserCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
):
    try:
        create(session, new_user)
        return Message(content='CREATED')

    except AlreadyExistsError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=err.message
        )
