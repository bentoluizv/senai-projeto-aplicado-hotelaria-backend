from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_session
from app.database.models import AccommodationDB, BookingDB, GuestDB
from app.domain.Booking import Booking, BookingDTO, BookingList

router = APIRouter(tags=['Reservas'], prefix='/reservas')


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Booking,
)
async def create_booking(
    booking_dto: BookingDTO, session: Session = Depends(get_session)
):
    exists = session.scalar(
        select(BookingDB).where(BookingDB.locator == booking_dto.locator)
    )

    if exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Booking already exists'
        )

    db_guest = session.get(GuestDB, booking_dto.guest_document)
    db_accommodation = session.get(
        AccommodationDB, booking_dto.accommodation_id
    )

    if not db_guest or not db_accommodation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Guest or Accommodation does not exist',
        )

    # TODO: VERIFICAR SE NÃO EXISTEM OUTRAS RESERVAS COM  O HORÁRIO CONFLITANDO

    db_booking = BookingDB(
        uuid=str(uuid4()),
        created_at=datetime.now().isoformat(),
        locator=booking_dto.locator,
        check_in=booking_dto.check_in,
        check_out=booking_dto.check_out,
        budget=booking_dto.budget,
        status=booking_dto.status,
        guest_document=booking_dto.guest_document,
        accommodation_id=booking_dto.accommodation_id,
        guest=db_guest,
        accommodation=db_accommodation,
    )

    session.add(db_booking)
    session.commit()

    return db_booking


@router.get('/', status_code=HTTPStatus.OK, response_model=BookingList)
async def list_all_bookings(session: Session = Depends(get_session)):
    db_bookings = session.scalars(select(BookingDB)).all()
    return {'bookings': db_bookings}


@router.get('/{uuid}', status_code=HTTPStatus.OK, response_model=Booking)
async def find_booking(uuid: str, session: Session = Depends(get_session)):
    db_booking = session.get(BookingDB, uuid)

    if not db_booking:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
        )
    return db_booking


@router.put('/{uuid}', status_code=HTTPStatus.OK, response_model=Booking)
async def update_booking(
    uuid: str, booking_dto: BookingDTO, session: Session = Depends(get_session)
):
    db_booking = session.get(BookingDB, uuid)

    if not db_booking:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
        )

    db_booking.locator = booking_dto.locator
    db_booking.status = booking_dto.status
    db_booking.check_in = booking_dto.check_in
    db_booking.check_out = booking_dto.check_out
    db_booking.budget = booking_dto.budget

    if db_booking.guest_document != booking_dto.guest_document:
        db_guest = session.get(GuestDB, booking_dto.guest_document)
        if not db_guest:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Guest not found in booking [{db_booking.locator}]',
            )
        db_booking.guest_document = db_guest.document
        db_booking.guest = db_guest

    if db_booking.accommodation_id != booking_dto.accommodation_id:
        db_accommodation = session.get(
            AccommodationDB, booking_dto.accommodation_id
        )
        if not db_accommodation:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"""
                Accommodation not found in booking [{db_booking.locator}]
            """,
            )
        db_booking.accommodation_id = db_accommodation.id
        db_booking.accommodation = db_accommodation

        return db_booking


@router.delete('/{uuid}', status_code=HTTPStatus.NO_CONTENT)
async def delete_booking(uuid: str, session: Session = Depends(get_session)):
    db_booking = session.get(BookingDB, uuid)

    if not db_booking:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
        )
