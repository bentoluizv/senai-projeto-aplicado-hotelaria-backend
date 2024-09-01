from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.db import get_database_session
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO
from app.services.guests import (
    create,
    delete,
    find_by_id,
    list_all,
    update,
)

router = APIRouter(tags=['Hóspedes'], prefix='/guests')


class Message(BaseModel):
    content: str


@router.get('/', status_code=HTTPStatus.OK, response_model=list[GuestDB])
async def list_all_guests(
    session: Annotated[Session, Depends(get_database_session)],
):
    guests = list_all(session)

    return guests


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_guest(
    new_guest: GuestCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
):
    try:
        create(session, new_guest)
        return Message(content='CREATED')

    except AlreadyExistsError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=err.message
        )


@router.get(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=GuestDB,
)
async def find_guest(
    id: str, session: Annotated[Session, Depends(get_database_session)]
):
    try:
        guest = find_by_id(session, id)
        return guest

    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=err.message
        )


@router.put(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=GuestDB,
)
async def update_guest(
    uuid: str,
    data: GuestUpdateDTO,
    session: Annotated[Session, Depends(get_database_session)],
):
    try:
        guest = update(session, uuid, data)
        return guest

    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=err.message
        )


@router.delete('/{uuid}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_guest(
    uuid: str, session: Annotated[Session, Depends(get_database_session)]
):
    try:
        delete(session, uuid)
        return Message(content='DELETED')

    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=err.message
        )
