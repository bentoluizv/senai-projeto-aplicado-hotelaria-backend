import pytest
from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db


@pytest.fixture
def accommodation_dao(app):
    with app.app_context():
        db = get_db()
        dao = AccommodationDAO(db)
        yield dao


def test_should_count_the_number_of_rows(accommodation_dao):
    assert accommodation_dao.count() == 6


def test_should_create_an_accommodation(accommodation_dao):
    accommodation_dto = {
        "name": "Quarto Individual",
        "status": "Disponivel",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "created_at": "2024-05-22T10:56:45.439704",
        "amenities": ["ducha", "wifi"],
    }

    accommodation_dao.insert(accommodation_dto)

    assert accommodation_dao.count() == 7


def test_should_return_one_accommodation_by_its_uuid(accommodation_dao):
    accommodation = accommodation_dao.findBy("id", 1)
    assert accommodation["name"] == "Domo"
    assert "amenities" in accommodation


def test_should_return_all_accommodations(accommodation_dao):
    data = accommodation_dao.find_many()
    assert len(data) == 6
    assert data[0]["amenities"]


def test_should_update_one_accommodation(accommodation_dao):
    accommodation_dto = {
        "name": "Quarto Individual",
        "status": "Disponivel",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "amenities": ["ducha", "wifi"],
    }

    accommodation_dao.update(1, accommodation_dto)
    result = accommodation_dao.findBy("id", 1)
    assert result["name"] == "Quarto Individual"


def test_should_delete_one_accommodation_by_its_uuid(accommodation_dao):
    accommodation_dao.delete(1)
    res = accommodation_dao.findBy("id", 1)
    assert res is None
