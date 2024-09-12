from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.db import get_database_session
from app.infra.database.models import AccommodationDB
from app.schemas.Accommodation import (
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.schemas.Accommodation import AccommodationCreateDTO
from app.services.accommodations import (
    create,
    delete,
    find_by_id,
    list_all,
    update,
)

router = APIRouter(tags=['Acomodações'], prefix='/acomodacoes')

class Message(BaseModel):
    content: str


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=tuple[AccommodationDB]
)
async def list_all_accommodations(
    session: Annotated[Session, Depends(get_database_session)],
): 
    accommodation = list_all(session)

    return accommodation



@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
async def create_accommodation(
    new_accommodation: AccommodationCreateDTO,
    session: Session = Depends(get_database_session),
): 
    try:
        create(session, new_accommodation)
        return Message(content='CREATED')

    except AlreadyExistsError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=err.message
        )




@router.get(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=AccommodationDB,
)
async def find_accommodation(
    id: str, session: Session = Depends(get_database_session)
): 
    try:
        accommodation = find_by_id(session, id)
        return accommodation

    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=err.message
        )


@router.put(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=AccommodationDB,
)
async def update_accommodation(
    id: str,
    accommodation_dto: AccommodationUpdateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): 
    try:
        accommodation = update(session, id, accommodation_dto)
        return accommodation

    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=err.message
        )


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_accommodation(
    id: int,
       session: Annotated[
        Session,
        Depends(get_database_session),
    ],
): 
    try:
        delete(session, id)
        return Message(content='DELETED')

    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=err.message
        )