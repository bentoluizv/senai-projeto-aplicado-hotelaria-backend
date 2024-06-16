import json

import pytest
from app.entity.Accommodation import Accommodation
from click import echo


@pytest.fixture()
def accommodation_data():
    data = {
        "id": 1,
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "created_at": "2024-05-22T10:56:45.439704",
        "amenities": ["wifi", "ducha"],
    }
    yield data


def test_should_instanciate_a_valid_accommodation(accommodation_data):
    accommodation = Accommodation.from_dict(accommodation_data)
    assert isinstance(accommodation, Accommodation)


def test_should_serialize_correctly_to_an_equivalent_dict(accommodation_data):
    guest = Accommodation.from_dict(accommodation_data)
    guest_dict = guest.to_dict()
    assert guest_dict == accommodation_data


def test_should_serialize_correctly_to_a_json_equivalent(accommodation_data):
    accommodation = Accommodation.from_dict(accommodation_data)
    accommodation_json = accommodation.to_json()

    accommodation_data["created_at"] = accommodation_data["created_at"]
    echo(json.dumps(accommodation_data, separators=(",", ":")))
    assert accommodation_json == json.dumps(
        accommodation_data, separators=(",", ":"), ensure_ascii=False
    )


def test_should_raise_an_error_when_passing_an_empty_string_to_name(accommodation_data):
    accommodation_data["name"] = ""
    with pytest.raises(ValueError):
        Accommodation.from_dict(accommodation_data)


def test_should_raise_an_error_when_passing_either_single_and_double_beds(
    accommodation_data,
):
    accommodation_data["single_beds"] = 0
    accommodation_data["double_beds"] = 0
    with pytest.raises(ValueError):
        Accommodation.from_dict(accommodation_data)


def test_should_raise_an_error_when_price_is_less_or_equal_to_zero(
    accommodation_data,
):
    accommodation_data["price"] = 0
    with pytest.raises(ValueError):
        Accommodation.from_dict(accommodation_data)


def test_should_raise_an_error_when_min_nights_is_less_or_equal_to_zero(
    accommodation_data,
):
    accommodation_data["min_nights"] = 0
    with pytest.raises(ValueError):
        Accommodation.from_dict(accommodation_data)


def test_should_raise_an_error_when_status_is_not_valid(
    accommodation_data,
):
    accommodation_data["status"] = "<badformat>"
    with pytest.raises(ValueError):
        Accommodation.from_dict(accommodation_data)


def test_should_raise_an_error_when_reassigning_any_property(accommodation_data):
    accommodation = Accommodation.from_dict(accommodation_data)
    with pytest.raises(ValueError):
        accommodation.name = "Novo Quarto"
