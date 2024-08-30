from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infra.database.db import get_database_session
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO

router = APIRouter(tags=['Hóspedes'], prefix='/guests')


class Message(BaseModel):
    content: str


@router.get('/', status_code=HTTPStatus.OK, response_model=tuple[GuestDB])
async def list_all_guests(
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_guest(
    data: GuestCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.get(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=GuestDB,
)
async def find_guest(
    uuid: UUID, session: Annotated[Session, Depends(get_database_session)]
): ...


@router.put(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def update_guest(
    uuid: UUID,
    data: GuestUpdateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.delete('/{uuid}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_guest(
    uuid: UUID, session: Annotated[Session, Depends(get_database_session)]
): ...
