import datetime
from uuid import uuid4

import pytest
from sqlalchemy import select, update

from app.database.models import (
    AccommodationDB,
    BookingDB,
    GuestDB,
)


@pytest.mark.skip()
def test_create_booking(session):
    BUDGET = 12000

    new_booking = BookingDB(
        uuid=uuid4(),
        created_at=datetime.datetime.now(),
        status='Confirmado',
        locator='AH123208',
        check_in=datetime.datetime(2024, 12, 18),
        check_out=datetime.datetime(2025, 1, 4),
        budget=12000,
        accommodation_id=1,
        guest_document='45678912300',
        accommodation=session.get(AccommodationDB, 1),
        guest=session.get(GuestDB, '45678912300'),
    )

    session.add(new_booking)
    session.commit()

    booking = session.scalar(
        select(BookingDB).where(BookingDB.locator == 'AH123208')
    )
    assert booking.budget == BUDGET
    assert booking.guest.document == '45678912300'
    assert booking.accommodation.name == 'Domo'


@pytest.mark.skip()
def test_select_all_bookings(session):
    TOTAL_BOOKINGS = 2
    statement = select(BookingDB)
    db_bookings = session.scalars(statement).all()
    assert len(db_bookings) == TOTAL_BOOKINGS


@pytest.mark.skip()
def test_find_booking_by_locator(session):
    statement = select(BookingDB).where(BookingDB.locator == 'LOC123457')
    db_booking = session.scalar(statement)
    assert db_booking
    assert db_booking.guest.name == 'Maria'


@pytest.mark.skip()
def test_update_booking(session):
    NEW_BUDGET = 2800
    statement = (
        update(BookingDB)
        .where(BookingDB.locator == 'LOC123457')
        .values(budget=NEW_BUDGET)
    )
    session.execute(statement)

    statement = select(BookingDB).where(BookingDB.locator == 'LOC123457')

    booking_db = session.scalar(statement)
    assert booking_db
    assert booking_db.budget == NEW_BUDGET


@pytest.mark.skip()
def test_delete_accommodation(session):
    accommodation_db = session.get(
        BookingDB, 'b2a72d82-71e1-11e9-8f9e-2a86e4085a59'
    )
    session.delete(accommodation_db)

    statement = select(BookingDB).where(BookingDB.locator == 'LOC123457')
    exists = session.scalar(statement)
    assert not exists
