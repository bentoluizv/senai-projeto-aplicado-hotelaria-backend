import json

import pytest

from app.entity.Guests import Guest


@pytest.fixture()
def guest_data():
    data = {
        "document": "03093331056",
        "name": "John",
        "surname": "Doe",
        "phone": "4832395853",
        "country": "Brazil",
        "created_at": "2024-05-22T10:56:45.439704",
    }

    yield data


def test_should_instanciate_a_valid_guest(guest_data):
    guest = Guest.from_dict(guest_data)
    assert isinstance(guest, Guest)


def test_should_serialize_correctly_to_an_equivalent_dict(guest_data):
    guest = Guest.from_dict(guest_data)
    guest_dict = guest.to_dict()
    assert guest_dict == guest_data


def test_should_serialize_correctly_to_a_json_equivalent(guest_data):
    guest = Guest.from_dict(guest_data)
    guest_data["created_at"] = guest_data["created_at"]
    data_json = json.dumps(guest_data, separators=(",", ":"))
    guest_json = guest.to_json()
    assert guest_json == data_json


def test_should_raise_an_error_when_passing_created_at_with_a_string_not_in_iso_format(
    guest_data,
):
    guest_data["created_at"] = ""
    with pytest.raises(ValueError):
        Guest.from_dict(guest_data)


def test_should_raise_an_error_when_passing_document_with_an_invalid_cpf(guest_data):
    guest_data["document"] = "03093331051"
    with pytest.raises(ValueError):
        Guest.from_dict(guest_data)


def test_should_raise_an_error_when_passing_any_property_as_an_empty_string(guest_data):
    guest_data["name"] = ""
    with pytest.raises(ValueError):
        Guest.from_dict(guest_data)


def test_should_raise_an_error_when_reassigning_any_property(guest_data):
    guest = Guest.from_dict(guest_data)
    with pytest.raises(ValueError):
        guest.name = "Derick"
