from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.db import get_database_session
from app.schemas.Message import Message
from app.schemas.User import UserCreateDTO

router = APIRouter(tags=['Users'], prefix='/users')


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_users(
    new_user: UserCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...
