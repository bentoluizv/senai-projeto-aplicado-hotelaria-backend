from datetime import datetime

import click
from pytest import fixture
import pytest
from app.data.dao.accommodation_dao import AccommodationDAO
from app.data.database.db import get_db
from app.domain.Accomodation import Accommodation, AccommodationDTO

@fixture
def accommodation_dao(app):
    with app.app_context():
        db = get_db()
        dao = AccommodationDAO(db)
        yield dao


def test_accommodation_dao_count(accommodation_dao):
    count = accommodation_dao.count()
    assert count == 6


def test_accommodation_dao_find_many(accommodation_dao):
    accommodations = accommodation_dao.find_many()
    assert len(accommodations) == 6


def test_accommodation_dao_find(accommodation_dao):
    acc = accommodation_dao.find("bcadaaf8-a036-42d5-870c-de7b24792abf")
    assert acc.name == 'Domo'
    assert len(acc.amenities) == 7



def test_accommodation_dao_insert(accommodation_dao):
    accommodation_dto: AccommodationDTO = {
        'status': "Disponivel",
        'name': "Quarto",
        'total_guests': 1,
        'single_beds': 1,
        'double_beds': 0,
        'min_nights': 2,
        'price': 150,
        'uuid': None,
        'created_at': None,
        'amenities': ['wifi', 'ducha']
    }
    accommodation = Accommodation(accommodation_dto)
    accommodation_dao.insert(accommodation)
    acc = accommodation_dao.find(accommodation.uuid)
    assert acc is not None
    assert acc.name == 'Quarto'


def test_accommodation_dao_update(accommodation_dao):
    accommodation_dto: AccommodationDTO = {
        'status': "Disponivel",
        'name': "Domo",
        'total_guests': 3,
        'single_beds': 0,
        'double_beds': 1,
        'min_nights': 2,
        'price': 850,
        'uuid': 'bcadaaf8-a036-42d5-870c-de7b24792abf',
        'created_at': '2000-01-01T00:00:00',
        'amenities': ['wifi', 'ducha']
    }
    acc = accommodation_dao.find('bcadaaf8-a036-42d5-870c-de7b24792abf')
    assert acc.name == 'Domo'
    assert acc.price == 590
    accommodation_dao.update(Accommodation(accommodation_dto))
    acc_updated = accommodation_dao.find('bcadaaf8-a036-42d5-870c-de7b24792abf')
    assert acc_updated.name == 'Domo'
    assert acc_updated.price == 850


def test_accommodation_dao_delete(accommodation_dao):
    accommodation_dao.delete('bcadaaf8-a036-42d5-870c-de7b24792abf')
    result = accommodation_dao.find('bcadaaf8-a036-42d5-870c-de7b24792abf')
    assert result is None