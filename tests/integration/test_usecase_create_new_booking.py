from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.database.models import BookingDB
from app.domain.Booking import BookingCreationalDTO
from app.services.createNewBooking import createNewBooking


def test_create_booking(session):
    data = {
        'status': 'Confirmada',
        'check_in': datetime(2024, 12, 8).isoformat(),
        'check_out': datetime(2024, 12, 12).isoformat(),
        'budget': 8200,
        'guest_document': '45678912300',
        'accommodation_id': 1,
    }

    data = BookingCreationalDTO(**data)

    booking = createNewBooking(session, data)
    assert booking.guest.document == '45678912300'
    assert booking.status == 'Confirmada'
    assert session.scalar(
        select(BookingDB).where(BookingDB.locator == booking.locator)
    )


def test_create_booking_raise_check_in_conflit(session):
    data = {
        'status': 'Confirmada',
        'check_in': datetime(2024, 7, 2).isoformat(),
        'check_out': datetime(2024, 7, 7).isoformat(),
        'budget': 8200,
        'guest_document': '45678912300',
        'accommodation_id': 1,
    }

    data = BookingCreationalDTO(**data)

    with pytest.raises(HTTPException):
        createNewBooking(session, data)


def test_create_booking_raise_check_out_conflit(session):
    data = {
        'status': 'Confirmada',
        'check_in': datetime(2024, 2, 2).isoformat(),
        'check_out': datetime(2024, 7, 4).isoformat(),
        'budget': 8200,
        'guest_document': '45678912300',
        'accommodation_id': 1,
    }

    data = BookingCreationalDTO(**data)

    with pytest.raises(HTTPException):
        createNewBooking(session, data)
