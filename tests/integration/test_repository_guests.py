import pytest
from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.data.repositories.GuestRepository import GuestRepository
from app.entity.Guests import Guest
from app.errors.NotFoundError import NotFoundError


@pytest.fixture
def repository(app):
    with app.app_context():
        db = get_db()
        dao = GuestDAO(db)
        repository = GuestRepository(dao)
        yield repository


def test_repository_count(repository):
    assert repository.count() == 4


def test_repository_insert(repository):
    data = {
        "document": "03093331056",
        "name": "Ana Claudia",
        "surname": "Costa",
        "country": "Brazil",
        "phone": "4832395853",
        "created_at": "2024-05-22T10:56:45.439704",
    }

    guest = Guest.from_dict(data)

    repository.insert(guest)
    assert repository.count() == 5


def test_repository_select(repository):
    guest = repository.findBy("document", "00157624242")
    assert guest.name == "Bento"


def test_repository_select_many(repository):
    res = repository.find_many()
    assert len(res) == 4
    assert isinstance(res[0], Guest)


def test_repository_update(repository):
    guest_dto = {
        "document": "00157624242",
        "name": "Bento Luiz",
        "surname": "V M da S Neto",
        "country": "Brazil",
        "phone": " 4832395853",
    }
    guest_to_update = Guest.from_dict(guest_dto)
    repository.update(guest_to_update)
    guest = repository.findBy("document", "00157624242")
    assert guest.surname == "V M da S Neto"


def test_repository_delete(repository):
    repository.delete("00157624242")
    with pytest.raises(NotFoundError):
        repository.findBy("document", "00157624242")
