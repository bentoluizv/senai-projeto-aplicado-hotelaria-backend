from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.domain.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.infra.database.db import get_database_session

router = APIRouter(tags=['Acomodações'], prefix='/acomodacoes')


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Accommodation,
)
async def create_accommodation(
    accommodation_dto: AccommodationCreateDTO,
    session: Session = Depends(get_database_session),
): ...


@router.get('/', status_code=HTTPStatus.OK, response_model=list[Accommodation])
async def list_all_accommodations(
    session: Session = Depends(get_database_session),
): ...


@router.get(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=Accommodation,
)
async def find_accommodation(
    id: str, session: Session = Depends(get_database_session)
): ...


@router.put(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=Accommodation,
)
async def update_accommodation(
    id: str,
    accommodation_dto: AccommodationUpdateDTO,
    session: Session = Depends(get_database_session),
): ...


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_accommodation(
    id: int, session: Session = Depends(get_database_session)
): ...
