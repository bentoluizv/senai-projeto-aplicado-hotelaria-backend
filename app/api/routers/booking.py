from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_session
from app.database.models import AccommodationDB, BookingDB, GuestDB
from app.domain.Booking import (
    Booking,
    BookingCreationalDTO,
    BookingUpdateDTO,
)
from app.utils.generate_locator import generate_locator

router = APIRouter(tags=['Reservas'], prefix='/reservas')


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Booking,
)
async def create_booking(
    booking_dto: BookingCreationalDTO, session: Session = Depends(get_session)
):
    db_guest = session.get(GuestDB, booking_dto.guest_document)
    db_accommodation = session.get(
        AccommodationDB, booking_dto.accommodation_id
    )

    if not db_guest:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Guest does not exist',
        )

    if not db_accommodation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Accommodation does not exist',
        )

    if db_accommodation.status in {'Ocupada', 'Aguardando Reserva'}:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Accommodation already booked',
        )

    db_booking = BookingDB(
        uuid=str(uuid4()),
        created_at=datetime.now().isoformat(),
        locator=generate_locator(),
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


@router.get('/', status_code=HTTPStatus.OK)
async def list_all_bookings(session: Session = Depends(get_session)):
    db_bookings = session.scalars(select(BookingDB)).all()
    return {'bookings': db_bookings}


@router.get('/{identifier}', status_code=HTTPStatus.OK, response_model=Booking)
async def find_booking(
    identifier: str, session: Session = Depends(get_session)
):
    UUID_LENGTH = 36
    if len(identifier) == UUID_LENGTH:
        db_booking = session.get(BookingDB, identifier)

        if not db_booking:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
            )

        return db_booking

    else:
        db_booking = session.scalar(
            select(BookingDB).where(BookingDB.locator == identifier)
        )
        if not db_booking:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
            )

        return db_booking


@router.put('/{uuid}', status_code=HTTPStatus.NO_CONTENT)
async def update_booking(
    uuid: str,
    booking_dto: BookingUpdateDTO,
    session: Session = Depends(get_session),
):
    db_booking = session.get(BookingDB, uuid)

    if not db_booking:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
        )

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


@router.delete('/{uuid}', status_code=HTTPStatus.NO_CONTENT)
async def delete_booking(uuid: str, session: Session = Depends(get_session)):
    db_booking = session.get(BookingDB, uuid)

    if not db_booking:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Booking not found'
        )
