import pytest

from app.data.dao.BookingDAO import BookingDAO
from app.data.database.db import get_db
from app.data.repositories.BookingRepository import BookingRepository
from app.entity.Booking import Booking
from app.errors.NotFoundError import NotFoundError


@pytest.fixture
def repository(app):
    with app.app_context():
        db = get_db()
        dao = BookingDAO(db)
        repository = BookingRepository(dao)
        yield repository


def test_should_count_how_many_records_are_registered(repository):
    assert repository.count() == 4


def test_should_create_a_new_booking(repository):
    booking_dto = {
        "uuid": "dd093495-b637-4ff8-bf2c-eb99d0f88031",
        "created_at": "2024-06-03T18:38:35.447990",
        "status": "Aguardando Check-In",
        "check_in": "2024-09-15T08:30:00",
        "check_out": "2024-09-18T12:30:00",
        "guest": {
            "document": "00157624242",
            "name": "Bento Luiz",
            "surname": "Vervloet Machado da Silva Neto",
            "country": "Brazil",
            "created_at": "2024-03-15T10:30:00",
            "phone": "48992054211",
        },
        "accommodation": {
            "id": 1,
            "name": "Domo",
            "status": "Disponível",
            "total_guests": 2,
            "single_beds": 0,
            "double_beds": 1,
            "min_nights": 2,
            "price": 590,
            "created_at": "2000-01-01T00:00:00",
            "amenities": [
                "ar-condicionado",
                "wifi",
                "tv",
                "frigobar",
                "ducha",
                "cozinha",
                "toalhas",
            ],
        },
    }
    booking = Booking.from_dict(booking_dto)
    repository.insert(booking)
    assert repository.count() == 5


def test_should_find_a_booking_by_its_uuid(repository):
    booking = repository.findBy("uuid", "e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    assert booking.guest.name == "Bento"


def test_should_return_all_bookings_registered(repository):
    bookings = repository.find_many()
    assert len(bookings) == 4
    assert bookings[0].guest.name == "Bento"


def test_shoud_update_an_existing_booking(repository):
    updated_booking_data = {
        "uuid": "e08f76e8-0e71-4a48-a85a-bf7e8f61479e",
        "status": "Finalizada",
        "check_in": "2024-06-15T08:30:00",
        "check_out": "2024-06-18T17:30:00",
        "guest": {
            "document": "00157624242",
            "name": "Bento Luiz",
            "surname": "Vervloet Machado da Silva Neto",
            "country": "Brazil",
            "created_at": "2024-03-15T10:30:00",
            "phone": "48992054211",
        },
        "accommodation": {
            "id": 6,
            "name": "Estacionamento para overlanders",
            "status": "Disponível",
            "total_guests": 4,
            "single_beds": 0,
            "double_beds": 0,
            "min_nights": 2,
            "price": 100,
            "created_at": "2000-01-01T00:15:00",
            "amenities": ["ducha"],
        },
    }

    booking = Booking.from_dict(updated_booking_data)
    repository.update(booking)
    updated_booking = repository.findBy("uuid", "e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    assert updated_booking.status == "Finalizada"


def test_repository_delete(repository):
    repository.delete("e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    with pytest.raises(NotFoundError):
        repository.findBy("uuid", "e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
