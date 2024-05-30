from pytest import fixture
import pytest
from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation

@fixture
def repository(app):
    with app.app_context():
        db = get_db()
        dao = AccommodationDAO(db)
        repository = AccommodationtRepository(dao)
        yield repository



def test_should_count_the_numbers_rows(repository):
    assert repository.count() == 6


def test_should_create_a_accommodation(repository):
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

    accommodation = Accommodation.from_dict(accommodation_dto)
    repository.insert(accommodation)

    assert repository.count() == 7


def test_should_return_one_accommodation_by_its_name(repository):
    guest = repository.findBy("name", "Domo")
    assert guest.uuid == 'bcadaaf8-a036-42d5-870c-de7b24792abf'


def test_should_return_all_accommodations(repository):
    res = repository.find_many()
    assert len(res) == 6
    assert isinstance(res[0], Accommodation)


def test_repository_update(repository):
    accommodation_dto = {
        'uuid': "bcadaaf8-a036-42d5-870c-de7b24792abf",
        'name':'Quarto Individual',
        'status':'Disponivel',
        'total_guests': '1',
        'single_beds': '1',
        'double_beds': '0',
        'min_nights': '2',
        'price':'180',
        }
    accommodation_to_update =  Accommodation.from_dict(accommodation_dto)
    repository.update(accommodation_to_update)
    accommodation = repository.findBy("uuid","bcadaaf8-a036-42d5-870c-de7b24792abf")
    assert accommodation.name == 'Quarto Individual'


def test_should_delete_one_accommodation_by_its_uuid(repository):
    repository.delete("bcadaaf8-a036-42d5-870c-de7b24792abf")
    with pytest.raises(ValueError):
        repository.findBy("uuid", "bcadaaf8-a036-42d5-870c-de7b24792abf")