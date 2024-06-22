import pytest

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.schemas.AccommodationSchema import (
    AccommodationCreationalSchema,
    AccommodationDB,
)
from app.data.database.sqlite.db import get_db
from app.data.repository.AccommodationRepository import AccommodationRepository
from app.errors.NotFoundError import NotFoundError


@pytest.fixture()
def accommodation_repository(app):
    with app.app_context():
        db = get_db()
        dao = AccommodationDAO(db)
        accommodation_repository = AccommodationRepository(dao)
        yield accommodation_repository


def test_accommodation_repository_find_many(accommodation_repository):
    TOTAL_ACCOMMODATIONS = 6
    accommodations = accommodation_repository.find_many()
    assert len(accommodations) == TOTAL_ACCOMMODATIONS


def test_accommodation_repository_find(accommodation_repository):
    accommodation = accommodation_repository.find(1)
    assert accommodation
    assert accommodation.name == 'Domo'


def test_accommodation_repository_find_by(accommodation_repository):
    accommodation = accommodation_repository.find_by('name', 'Domo')
    assert accommodation
    assert accommodation[0].id == 1


def test_accommodation_repository_create(accommodation_repository):
    data = AccommodationCreationalSchema(**{
        'name': 'Churrasqueira',
        'status': 'Disponivel',
        'total_guests': 6,
        'single_beds': 0,
        'double_beds': 2,
        'price': 350,
        'amenities': ['wifi', 'ducha'],
    })
    accommodation_repository.create(data)
    accomodation = accommodation_repository.find_by('name', 'Churrasqueira')
    assert accomodation
    assert 'wifi' in accomodation[0].amenities


def test_accommodation_repository_update(accommodation_repository):
    data = {
        'id': 1,
        'name': 'Domo',
        'status': 'Aguardando Check-in',
        'total_guests': 6,
        'single_beds': 0,
        'double_beds': 2,
        'price': 850,
        'amenities': ['wifi', 'ducha', 'toalhas'],
    }

    accommodation_repository.update(AccommodationDB(**data))
    accommodation = accommodation_repository.find_by('name', 'Domo')
    assert accommodation[0].status == 'Aguardando Check-in'


def test_accommodation_repository_delete(accommodation_repository):
    accommodation_repository.delete(1)
    with pytest.raises(NotFoundError):
        accommodation_repository.find(1)
