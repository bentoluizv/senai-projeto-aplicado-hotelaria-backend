import datetime
from uuid import uuid4

from sqlalchemy import select, update

from app.database.sqlalchemy.models import (
    AccommodationDB,
    BookingDB,
    GuestDB,
)


def test_create_booking(session):
    BUDGET = 12000

    new_booking = BookingDB(
        uuid=str(uuid4()),
        created_at=datetime.datetime.now().isoformat(),
        status='Confirmado',
        locator='AH123208',
        check_in=datetime.datetime(2024, 12, 18).isoformat(),
        check_out=datetime.datetime(2025, 1, 4).isoformat(),
        budget=12000,
        accommodation_id=1,
        guest_document='456.789.123-00',
        accommodation=session.get(AccommodationDB, 1),
        guest=session.get(GuestDB, '456.789.123-00'),
    )

    session.add(new_booking)
    session.commit()

    booking = session.scalar(
        select(BookingDB).where(BookingDB.locator == 'AH123208')
    )
    assert booking.budget == BUDGET
    assert booking.guest.document == '456.789.123-00'
    assert booking.accommodation.name == 'Domo'


def test_select_all_bookings(session):
    TOTAL_BOOKINGS = 2
    statement = select(BookingDB)
    db_bookings = session.scalars(statement).all()
    assert len(db_bookings) == TOTAL_BOOKINGS


def test_find_booking_by_locator(session):
    statement = select(BookingDB).where(BookingDB.locator == 'LOC123457')
    db_booking = session.scalar(statement)
    assert db_booking
    assert db_booking.guest.name == 'Maria'


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


def test_delete_accommodation(session):
    accommodation_db = session.get(
        BookingDB, 'b2a72d82-71e1-11e9-8f9e-2a86e4085a59'
    )
    session.delete(accommodation_db)

    statement = select(BookingDB).where(BookingDB.locator == 'LOC123457')
    exists = session.scalar(statement)
    assert not exists
