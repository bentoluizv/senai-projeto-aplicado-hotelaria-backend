import json
from datetime import datetime
from uuid import UUID

import pytest
from click import echo

from app.entity.Accommodation import Accommodation


@pytest.fixture()
def accommodation_data():
    data = {
        "uuid": UUID("ff90f824-5938-4c1a-8ad1-d558dc776470"),
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "created_at": datetime.fromisoformat("2024-05-22T10:56:45.439704"),
        "amenities": [],
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
    accommodation_data["uuid"] = str(accommodation_data["uuid"])
    accommodation_data["created_at"] = accommodation_data["created_at"].isoformat()
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


def test_should_raise_an_error_when_passing_created_at_with_a_string_not_in_iso_format(
    accommodation_data,
):
    accommodation_data["created_at"] = "<badformat>"
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