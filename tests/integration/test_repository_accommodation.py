import pytest
from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.sqlite3.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation
from app.errors.NotFoundError import NotFoundError


@pytest.fixture
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
        "id": None,
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "created_at": "2024-05-22T10:56:45.439704",
        "amenities": [],
    }

    accommodation = Accommodation.from_dict(accommodation_dto)
    repository.insert(accommodation)

    assert repository.count() == 7


def test_should_return_one_accommodation_by_its_name(repository):
    accommodation = repository.findBy("name", "Domo")
    assert accommodation.id == 1


def test_should_return_all_accommodations(repository):
    res = repository.find_many()
    assert len(res) == 6
    assert isinstance(res[0], Accommodation)


def test_repository_update(repository):
    data = {
        "id": 1,
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "amenities": ["ducha"],
    }
    accommodation_to_update = Accommodation.from_dict(data)
    repository.update(accommodation_to_update)
    accommodation = repository.findBy("id", 1)
    assert accommodation.name == "Quarto Individual"


def test_should_delete_one_accommodation_by_its_uuid(repository):
    repository.delete(1)
    with pytest.raises(NotFoundError):
        repository.findBy("id", 1)
