from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.errors.AlreadyExistsError import AlreadyExistsError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infra.database.db import get_database_session
from app.infra.database.models import UserDB
from app.schemas.User import UserCreateDTO

from app.services.users import (
    create,     
)

router = APIRouter(tags=['Users'], prefix='/users')

class Message(BaseModel):
    content: str



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