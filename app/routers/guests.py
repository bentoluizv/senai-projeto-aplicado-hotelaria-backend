from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.db import get_database_session
from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO
from app.schemas.Message import Message
from app.services.guests import (
    create,
    delete,
    find_by_id,
    list_all,
    update,
)

router = APIRouter(tags=['Hóspedes'], prefix='/hospedes')


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
    create_or_error = create(session, new_guest)

    if isinstance(create_or_error, AlreadyExistsError):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=create_or_error.message
        )

    return Message(content='CREATED')


@router.get(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=GuestDB,
)
async def find_guest(
    uuid: str, session: Annotated[Session, Depends(get_database_session)]
):
    guest_or_error = find_by_id(
        session,
        UUID(uuid),
    )

    if isinstance(guest_or_error, NotFoundError):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=guest_or_error.message
        )

    return guest_or_error


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
    guest_or_error = update(session, UUID(uuid), data)

    if isinstance(guest_or_error, NotFoundError):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=guest_or_error.message
        )

    return guest_or_error


@router.delete('/{uuid}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_guest(
    uuid: str,
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
):
    result = delete(
        session,
        UUID(uuid),
    )

    if isinstance(result, NotFoundError):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=result.message
        )

    return Message(content='DELETED')
