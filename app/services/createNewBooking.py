from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import AccommodationDB, BookingDB, GuestDB
from app.domain.Accommodation import Accommodation
from app.domain.Amenitie import Amenitie
from app.domain.Booking import Booking, BookingCreationalDTO
from app.domain.Guest import Guest
from app.utils.generate_locator import generate_locator
from app.utils.time_in_range import time_in_range


def createNewBooking(session: Session, input: BookingCreationalDTO):
    db_guest = session.get(GuestDB, input.guest_document)
    db_accommodation = session.get(AccommodationDB, input.accommodation_id)

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

    new_booking = Booking(
        check_in=datetime.fromisoformat(input.check_in),
        check_out=datetime.fromisoformat(input.check_out),
        locator=generate_locator(),
        budget=input.budget,
        status=input.status,
        guest=Guest(
            document=db_guest.document,
            name=db_guest.name,
            surname=db_guest.surname,
            phone=db_guest.phone,
            country=db_guest.country,
        ),
        accommodation=Accommodation(
            id=db_accommodation.id,
            name=db_accommodation.name,
            status=db_accommodation.status,
            total_guests=db_accommodation.total_guests,
            single_beds=db_accommodation.single_beds,
            double_beds=db_accommodation.double_beds,
            min_nights=db_accommodation.min_nights,
            price=db_accommodation.price,
            amenities=[
                Amenitie(id=amenitie.id, name=amenitie.name)
                for amenitie in db_accommodation.amenities
            ],
        ),
    )

    existing_db_bookings = session.scalars(
        select(BookingDB)
        .where(BookingDB.accommodation_id == new_booking.accommodation.id)
        .filter(
            BookingDB.status != 'Finalizada',
        )
    ).all()

    for db_booking in existing_db_bookings:
        existing_booking = Booking(
            uuid=db_booking.uuid,
            check_in=datetime.fromisoformat(db_booking.check_in),
            check_out=datetime.fromisoformat(db_booking.check_out),
            locator=db_booking.locator,
            budget=db_booking.budget,
            status=db_booking.status,
            guest=Guest(
                document=db_booking.guest.document,
                name=db_booking.guest.name,
                surname=db_booking.guest.surname,
                phone=db_booking.guest.phone,
                country=db_booking.guest.country,
            ),
            accommodation=Accommodation(
                id=db_booking.accommodation.id,
                name=db_booking.accommodation.name,
                status=db_booking.accommodation.status,
                total_guests=db_booking.accommodation.total_guests,
                single_beds=db_booking.accommodation.single_beds,
                double_beds=db_booking.accommodation.double_beds,
                min_nights=db_booking.accommodation.min_nights,
                price=db_booking.accommodation.price,
                amenities=[
                    Amenitie(id=amenitie.id, name=amenitie.name)
                    for amenitie in db_booking.accommodation.amenities
                ],
            ),
        )

        if time_in_range(
            existing_booking.check_in,
            existing_booking.check_out,
            new_booking.check_in,
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Check-in conflict with some existing booking',
            )

        if time_in_range(
            existing_booking.check_in,
            existing_booking.check_out,
            new_booking.check_out,
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Checkout conflict with some existing booking',
            )

    new_booking.set_status('Confirmada')
    new_booking.calculate_budget()

    db_booking = BookingDB(
        uuid=new_booking.uuid,
        created_at=new_booking.created_at.isoformat(),
        locator=new_booking.locator,
        check_in=new_booking.check_in.isoformat(),
        check_out=new_booking.check_out.isoformat(),
        budget=new_booking.budget,
        status=new_booking.status,
        guest_document=new_booking.guest.document,
        accommodation_id=new_booking.accommodation.id,
        guest=db_guest,
        accommodation=db_accommodation,
    )

    session.add(db_booking)
    session.commit()

    return new_booking
