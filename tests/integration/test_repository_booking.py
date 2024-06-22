import pytest

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.BookingDAO import BookingDAO
from app.data.dao.GuestDAO import GuestDAO
from app.data.database.sqlite.db import get_db
from app.data.repository.BookingRepository import BookingRepository
from app.errors.NotFoundError import NotFoundError


@pytest.fixture()
def booking_repository(app):
    with app.app_context():
        db = get_db()
        booking_dao = BookingDAO(db)
        accommodation_dao = AccommodationDAO(db)
        guest_dao = GuestDAO(db)
        booking_repository = BookingRepository(
            booking_dao, accommodation_dao, guest_dao
        )
        yield booking_repository


def test_booking_repository_find_many(booking_repository):
    TOTAL_BOOKINGS = 4
    booking = booking_repository.find_many()
    assert len(booking) == TOTAL_BOOKINGS


def test_booking_repository_find(booking_repository):
    booking = booking_repository.find('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    assert booking
    assert booking.accommodation.name == 'Estacionamento para overlanders'


def test_booking_repository_find_by(booking_repository):
    booking = booking_repository.find_by('locator', 'AB897564')[0]
    assert booking
    assert booking.guest.name == 'Bento'


def test_booking_repository_create(booking_repository):
    data = {
        'locator': 'AS341243',
        'status': 'Finalizada',
        'check_in': '2024-02-27T10:30:00.156342',
        'check_out': '2024-03-03T10:30:00.156342',
        'guest_document': '00157624242',
        'accommodation_id': 1,
        'budget': 1200,
    }

    booking_repository.create(data)
    booking = booking_repository.find_by('locator', 'AS341243')[0]
    assert booking
    assert booking.status == 'Finalizada'


def test_booking_repository_update(booking_repository):
    data = {
        'uuid': 'e08f76e8-0e71-4a48-a85a-bf7e8f61479e',
        'locator': 'AB897564',
        'status': 'Finalizada',
        'created_at': '2024-06-18T17:30:00',
        'check_in': '2024-06-06T08:30:00',
        'check_out': '2024-06-18T10:30:00.156342',
        'guest_document': '00157624242',
        'accommodation_id': 6,
        'budget': 1200,
    }

    booking_repository.update(data)
    booking = booking_repository.find('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    assert booking.status == 'Finalizada'


def test_booking_repository_delete(booking_repository):
    booking_repository.delete('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    with pytest.raises(NotFoundError):
        booking_repository.find('e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
