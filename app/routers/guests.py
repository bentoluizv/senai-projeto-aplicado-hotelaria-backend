from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.data.database.db import get_database_session
from app.data.repositories.GuestRepository import GuestRepository
from app.domain.errors.AlreadyExistsError import AlreadyExistsError
from app.domain.errors.NotFoundError import NotFoundError
from app.domain.Guest import Guest, GuestCreateDTO, GuestUpdateDTO

router = APIRouter(tags=['Hóspedes'], prefix='/guests')


class Message(BaseModel):
    content: str


@router.get('/', status_code=HTTPStatus.OK, response_model=list[Guest])
async def list_all_guests(
    session: Annotated[Session, Depends(get_database_session)],
) -> list[Guest]:
    repository = GuestRepository(session)
    guests = repository.list()
    return guests


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_guest(
    data: GuestCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
) -> Message:
    try:
        repository = GuestRepository(session)
        repository.insert(data)
        return Message(content='CREATED')

    except AlreadyExistsError as error:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=error.message
        )


@router.get(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=Guest,
)
async def find_guest(
    uuid: UUID, session: Annotated[Session, Depends(get_database_session)]
) -> Guest:
    try:
        repository = GuestRepository(session)
        guest = repository.find_by_id(uuid)
        return guest

    except NotFoundError as error:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=error.message
        )


@router.put(
    '/{uuid}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def update_guest(
    uuid: UUID,
    data: GuestUpdateDTO,
    session: Annotated[Session, Depends(get_database_session)],
):
    try:
        repository = GuestRepository(session)
        repository.update(uuid, data)
        return Message(content='UPDATED')

    except NotFoundError as error:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=error.message
        )


@router.delete('/{uuid}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_guest(
    uuid: UUID, session: Annotated[Session, Depends(get_database_session)]
):
    try:
        repository = GuestRepository(session)
        repository.delete(uuid)
        return Message(content='DELETED')

    except NotFoundError as error:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=error.message
        )
