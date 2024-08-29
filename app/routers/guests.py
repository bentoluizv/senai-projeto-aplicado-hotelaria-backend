from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.domain.Guest import Guest, GuestCreateDTO, GuestUpdateDTO
from app.infra.database.db import get_database_session

router = APIRouter(tags=['Hóspedes'], prefix='/guests')


class Message(BaseModel):
    content: str


@router.get('/', status_code=HTTPStatus.OK, response_model=list[Guest])
async def list_all_guests(
    session: Annotated[Session, Depends(get_database_session)],
) -> list[Guest]: ...


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_guest(
    data: GuestCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
) -> Message: ...


@router.get(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=Guest,
)
async def find_guest(
    uuid: UUID, session: Annotated[Session, Depends(get_database_session)]
) -> Guest: ...


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
