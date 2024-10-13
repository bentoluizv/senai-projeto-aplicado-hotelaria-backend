from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.db import get_database_session
from app.infra.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO
from app.schemas.Message import Message

router = APIRouter(tags=['Hóspedes'], prefix='/hospedes')


@router.get('/', status_code=HTTPStatus.OK, response_model=list[GuestDB])
async def list_all_guests(
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_guest(
    new_guest: GuestCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.get(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=GuestDB,
)
async def find_guest(
    uuid: str, session: Annotated[Session, Depends(get_database_session)]
): ...


@router.put(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=GuestDB,
)
async def update_guest(
    uuid: str,
    data: GuestUpdateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.delete('/{uuid}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_guest(
    uuid: str,
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
): ...
