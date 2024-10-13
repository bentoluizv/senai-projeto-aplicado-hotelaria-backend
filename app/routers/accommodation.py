from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.db import get_database_session
from app.infra.models import AccommodationDB
from app.schemas.Accommodation import (
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.schemas.Message import Message

router = APIRouter(tags=['Acomodações'], prefix='/accommodations')


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=list[AccommodationDB]
)
async def list_all_accommodations(
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
async def create_accommodation(
    new_accommodation: AccommodationCreateDTO,
    session: Session = Depends(get_database_session),
): ...


@router.get(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=AccommodationDB,
)
async def find_accommodation(
    id: str, session: Session = Depends(get_database_session)
): ...


@router.put(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=AccommodationDB,
)
async def update_accommodation(
    id: str,
    data: AccommodationUpdateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.delete('/{id}', status_code=HTTPStatus.OK)
async def delete_accommodation(
    id: str,
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
): ...
