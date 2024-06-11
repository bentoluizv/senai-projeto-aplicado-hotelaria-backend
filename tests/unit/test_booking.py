import json
from datetime import datetime

import pytest

from app.entity.Booking import Booking


@pytest.fixture()
def booking_data():
    data = {
        "uuid": "dd093495-b637-4ff8-bf2c-eb99d0f88031",
        "created_at": "2024-06-03T18:38:35.447990",
        "status": "Aguardando Check-In",
        "check_in": "2024-09-15T08:30:00",
        "check_out": "2024-09-18T12:30:00",
        "guest": {
            "document": "03093331056",
            "name": "John",
            "surname": "Doe",
            "phone": "4832395853",
            "country": "Brazil",
            "created_at": "2024-05-22T10:56:45",
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
    yield data


def test_should_instanciate_a_valid_booking(booking_data):
    booking = Booking.from_dict(booking_data)
    assert isinstance(booking, Booking)


def test_should_serialize_correctly_to_an_equivalent_dict(booking_data):
    booking = Booking.from_dict(booking_data)
    booking_dict = booking.to_dict()

    assert booking_dict == booking_data


def test_should_serialize_correctly_to_a_json_equivalent(booking_data):
    booking = Booking.from_dict(booking_data)
    booking_json = booking.to_json()
    assert booking_json == json.dumps(
        booking_data,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
    )


def test_should_raise_an_error_when_status_is_not_valid(booking_data):
    booking_data["status"] = "<badformat>"
    with pytest.raises(ValueError):
        Booking.from_dict(booking_data)


def test_should_raise_an_error_if_check_out_date_is_before_check_in(booking_data):
    booking_data["check_in"] = datetime(2024, 12, 8)
    booking_data["check_out"] = datetime(2024, 12, 2)
    with pytest.raises(ValueError):
        Booking.from_dict(booking_data)
