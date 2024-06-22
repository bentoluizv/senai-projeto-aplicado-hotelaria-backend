import pytest

from app.data.dao.BookingDAO import BookingDAO
from app.data.dao.schemas.BookingSchema import (
    BookingCreationalSchema,
    BookingDB,
)
from app.data.database.sqlite.db import get_db


@pytest.fixture()
def booking_dao(app):
    with app.app_context():
        db = get_db()
        dao = BookingDAO(db)
        yield dao


def test_should_counts_all_records(booking_dao):
    TOTAL_BOOKINGS = 4
    count = booking_dao.count()
    assert count == TOTAL_BOOKINGS


def test_should_select_all_bookings(booking_dao):
    TOTAL_BOOKINGS = 4
    bookings = booking_dao.find_many()
    assert len(bookings) == TOTAL_BOOKINGS


def test_should_select_a_booking(booking_dao):
    ACCOMMODATION_ID = 6

    booking = booking_dao.find('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    assert booking.check_in == '2024-06-15T08:30:00'
    assert booking.guest_document == '00157624242'
    assert booking.accommodation_id == ACCOMMODATION_ID


def test_should_select_a_booking_by_property(booking_dao):
    ACCOMMODATION_ID = 6

    booking = booking_dao.find_by('locator', 'AB897564')
    assert booking[0].check_in == '2024-06-15T08:30:00'
    assert booking[0].guest_document == '00157624242'
    assert booking[0].accommodation_id == ACCOMMODATION_ID


def test_should_create_a_new_booking(booking_dao):
    data = {
        'locator': 'AS341243',
        'status': 'Finalizada',
        'check_in': '2024-02-27T10:30:00.156342',
        'created_at': '2024-05-31T14:06:32.287011',
        'uuid': '2a4d265b-2836-414a-9927-f0e1ca45fa84',
        'check_out': '2024-03-3T10:30:00.156342',
        'guest_document': '00157624242',
        'accommodation_id': 1,
        'budget': 1200,
    }

    booking_dao.create(BookingCreationalSchema(**data))
    TOTAL_BOOKINGS = 5
    count = booking_dao.count()
    assert count == TOTAL_BOOKINGS


def test_should_update_an_existing_booking(booking_dao):
    data = {
        'uuid': 'e08f76e8-0e71-4a48-a85a-bf7e8f61479e',
        'created_at': '2024-05-31T14:06:32.287011',
        'locator': 'ZA341145',
        'status': 'Finalizada',
        'check_in': '2024-06-15T08:30:00',
        'check_out': '2024-06-18T17:30:00',
        'guest_document': '00157624242',
        'accommodation_id': 3,
        'budget': 1200,
    }

    booking_dao.update(BookingDB(**data))

    booking = booking_dao.find('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')

    assert booking.status == 'Finalizada'


def test_should_delete_an_existing_booking(booking_dao):
    booking_dao.delete('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    booking = booking_dao.find('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    assert booking is None
