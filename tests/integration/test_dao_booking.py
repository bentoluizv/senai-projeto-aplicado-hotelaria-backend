from pytest import fixture

from app.data.dao.BookingDAO import BookingDAO
from app.data.database.db import get_db


@fixture
def booking_dao(app):
    with app.app_context():
        db = get_db()
        dao = BookingDAO(db)
        yield dao


def test_should_counts_all_records(booking_dao):
    count = booking_dao.count()
    assert count == 4


def test_should_create_a_new_booking(booking_dao):
    data = {
        "status": "Finalizada",
        "check_in": "2024-02-27T10:30:00.156342",
        "created_at": "2024-05-31T14:06:32.287011",
        "uuid": "2a4d265b-2836-414a-9927-f0e1ca45fa84",
        "check_out": "2024-03-3T10:30:00.156342",
        "guest_document": "00157624242",
        "accommodation_uuid": "bcadaaf8-a036-42d5-870c-de7b24792abf",
    }

    booking_dao.insert(data)
    count = booking_dao.count()
    assert count == 5


def test_should_select_a_booking(booking_dao):
    booking = booking_dao.findBy("document", "00157624242")
    assert booking["check_in"] == "2024-06-15T08:30:00"
    assert booking["guest"]["name"] == "Bento Luiz"
    assert booking["accommodation"]["name"] == "Estacionamento para overlanders"
    assert booking["accommodation"]["amenities"]


def test_should_select_all_bookings(booking_dao):
    bookings = booking_dao.find_many()
    assert len(bookings) == 4
    assert bookings[0]["guest"]["name"] == "Bento Luiz"
    assert bookings[0]["accommodation"]["name"] == "Estacionamento para overlanders"


def test_should_update_an_existing_booking(booking_dao):
    data = {
        "status": "Finalizada",
        "check_in": "2024-06-15T08:30:00",
        "check_out": "2024-06-18T17:30:00",
        "guest_document": "00157624242",
        "accommodation_uuid": "242d5665-aa90-429a-95d5-767515ff8ccc",
    }
    booking_dao.update("e08f76e8-0e71-4a48-a85a-bf7e8f61479e", data)

    booking = booking_dao.findBy("uuid", "e08f76e8-0e71-4a48-a85a-bf7e8f61479e")

    assert booking["status"] == "Finalizada"


def test_should_delet_an_existing_booking(booking_dao):
    booking_dao.delete("e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    booking = booking_dao.findBy("uuid", "e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    assert booking is None
