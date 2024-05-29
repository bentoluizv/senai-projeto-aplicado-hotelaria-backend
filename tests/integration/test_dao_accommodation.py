from pytest import fixture
import pytest
from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db

@fixture
def accommodation_dao(app):
    with app.app_context():
        db = get_db()
        dao = AccommodationDAO(db)
        yield dao


def test_should_count_the_numbers_rows(accommodation_dao):
    assert accommodation_dao.count() == 6


def test_should_create_a_accommodation(accommodation_dao):
    accommodation_dto = {
        'uuid': 'ff90f824-5938-4c1a-8ad1-d558dc776470',
        'name':'Quarto Individual',
        'status':'Disponivel',
        'total_guests': '1',
        'single_beds': '1',
        'double_beds': '0',
        'min_nights': '2',
        'price':'180',
        'created_at': '2024-05-22T10:56:45.439704'
        }

    accommodation_dao.insert(accommodation_dto)

    assert accommodation_dao.count() == 7


def test_should_return_one_accommodation_by_its_uuid(accommodation_dao):
    accommodation = accommodation_dao.find("bcadaaf8-a036-42d5-870c-de7b24792abf")
    assert accommodation['name'] == 'Domo'


def test_should_return_all_accommodations(accommodation_dao):
    res = accommodation_dao.find_many()
    assert len(res) == 6


def test_should_update_one_accommodation(accommodation_dao):
    accommodation_dto = {
        'name':'Quarto Individual',
        'status':'Disponivel',
        'total_guests': '1',
        'single_beds': '1',
        'double_beds': '0',
        'min_nights': '2',
        'price':'180',
        }

    accommodation_dao.update("bcadaaf8-a036-42d5-870c-de7b24792abf", accommodation_dto)
    result = accommodation_dao.find("bcadaaf8-a036-42d5-870c-de7b24792abf")
    assert result['name'] == 'Quarto Individual'


def test_should_delete_one_accommodation_by_its_uuid(accommodation_dao):
    accommodation_dao.delete("bcadaaf8-a036-42d5-870c-de7b24792abf")
    res = accommodation_dao.find("bcadaaf8-a036-42d5-870c-de7b24792abf")
    assert res is None