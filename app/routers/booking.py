from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.db import get_database_session
from app.infra.models import BookingDB
from app.schemas.Booking import BookingCreateDTO, BookingUpdateDTO

router = APIRouter(tags=['Reservas'], prefix='/reservas')


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=BookingDB,
)
async def create_booking(
    booking_dto: BookingCreateDTO,
    session: Session = Depends(get_database_session),
): ...


@router.get('/', status_code=HTTPStatus.OK)
async def list_all_bookings(
    session: Session = Depends(get_database_session),
): ...


@router.get(
    '/{identifier}', status_code=HTTPStatus.OK, response_model=BookingDB
)
async def find_booking(
    identifier: str, session: Session = Depends(get_database_session)
): ...


@router.put('/{uuid}', status_code=HTTPStatus.NO_CONTENT)
async def update_booking(
    uuid: str,
    booking_dto: BookingUpdateDTO,
    session: Session = Depends(get_database_session),
): ...


@router.delete('/{uuid}', status_code=HTTPStatus.NO_CONTENT)
async def delete_booking(
    uuid: str, session: Session = Depends(get_database_session)
): ...
