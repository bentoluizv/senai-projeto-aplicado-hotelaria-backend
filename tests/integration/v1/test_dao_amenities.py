import pytest

from app.database.sqlite.dao.AmenitieDAO import AmenitieDAO
from app.database.sqlite.db import get_db


@pytest.fixture()
def amenities_dao(app):
    with app.app_context():
        db = get_db()
        dao = AmenitieDAO(db)
        yield dao


def test_amenities_dao_count(amenities_dao):
    TOTAL_AMENITIES = 8

    assert amenities_dao.count() == TOTAL_AMENITIES


def test_amenities_dao_find_many(amenities_dao):
    TOTAL_AMENITIES = 8
    guests = amenities_dao.find_many()
    assert len(guests) == TOTAL_AMENITIES


def test_amenities_dao_find(amenities_dao):
    guest = amenities_dao.find(1)
    assert guest


def test_amenities_dao_find_by_name(amenities_dao):
    guest = amenities_dao.find_by_name('wifi')
    assert guest


def test_amenities_dao_create(amenities_dao):
    TOTAL_AMENITIES = 9

    amenities_dao.create('hidro')

    assert amenities_dao.count() == TOTAL_AMENITIES


def test_amenities_dao_delete(amenities_dao):
    amenities_dao.delete(4)
    res = amenities_dao.find(4)
    assert not res


def test_list_amenities_from_accommodation(amenities_dao):
    TOTAL_AMENITIES = 7
    res = amenities_dao.list_amenities_from_accommodation(1)
    assert res
    assert len(res) == TOTAL_AMENITIES
    assert res[2].name == 'tv'


def test_delete_amenitie_from_accommodation(amenities_dao):
    amenities_dao.delete_amenitie_from_accommodation(1, 3)
    result = [
        amentie_db.model_dump()
        for amentie_db in amenities_dao.list_amenities_from_accommodation(1)
    ]

    assert {'id': 3, 'name': 'tv'} not in result


def test_insert_amenitie_in_accommodation(amenities_dao):
    amenities_dao.insert_amenitie_in_accommodation(6, 2)
    result = [
        amentie_db.model_dump()
        for amentie_db in amenities_dao.list_amenities_from_accommodation(6)
    ]
    assert {'id': 2, 'name': 'wifi'} in result
