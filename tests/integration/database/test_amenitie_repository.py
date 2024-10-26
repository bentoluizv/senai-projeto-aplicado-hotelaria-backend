import pytest
from sqlalchemy import select

from app.database.models import AmenitieDB
from app.entities.Amenitie import Amenitie, AmenitieCreateDTO


@pytest.fixture()
def amenitie_repository(repository_factory):
    amenitie_repository = repository_factory.create_amenitie_respository()
    return amenitie_repository


def test_list_all_amenities(amenitie_repository):
    TOTAL_AMENITIES = 6
    amenities = amenitie_repository.list_all()
    assert len(amenities) == TOTAL_AMENITIES


def test_list_all_amenities_2_per_page(amenitie_repository):
    TOTAL_AMENITIES = 2
    amenities = amenitie_repository.list_all(per_page=2)
    assert len(amenities) == TOTAL_AMENITIES


def test_list_all_out_range_return_0(amenitie_repository):
    TOTAL_AMENITIES = 0
    guests = amenitie_repository.list_all(page=60, per_page=1)
    assert len(guests) == TOTAL_AMENITIES


def test_not_found_amenitie_by_name(amenitie_repository):
    existing = amenitie_repository.find_by_name('<amenitie>')
    assert not existing


def test_find_amenitie_by_name(amenitie_repository):
    amenitie = amenitie_repository.find_by_name('WiFi')
    assert amenitie


def test_create_amenitie(amenitie_repository, session):
    dto = AmenitieCreateDTO(
        name='Teste amenitie',
    )

    amenitie = Amenitie.create(dto)

    amenitie_repository.create(amenitie)

    amenitie_created = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
    )
    assert amenitie_created is not None
    assert amenitie_created.id


def test_create_2_amenities_in_a_row(amenitie_repository, session):
    dtos = [
        AmenitieCreateDTO(
            name='Teste amenitie',
        ),
        AmenitieCreateDTO(
            name='Teste amenitie 2',
        ),
    ]

    amenities = [Amenitie.create(dto) for dto in dtos]

    for amenitie in amenities:
        amenitie_repository.create(amenitie)

    db_amenitie_1 = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
    )
    db_amenitie_2 = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
    )
    assert db_amenitie_1
    assert db_amenitie_2
