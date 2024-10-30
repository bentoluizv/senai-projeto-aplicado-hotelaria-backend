import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.database.models import AccommodationDB
from app.entities.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
)
from app.entities.Amenitie import Amenitie


@pytest.fixture()
def accommodation_repository(repository_factory):
    accommodation_repository = (
        repository_factory.create_accommodation_respository()
    )
    return accommodation_repository


def test_list_all_accommodations(accommodation_repository):
    TOTAL_ACCOMMODATIONS = 10
    accommodation = accommodation_repository.list_all()
    assert len(accommodation) == TOTAL_ACCOMMODATIONS


def test_list_all_accommodations_2_per_page(accommodation_repository):
    TOTAL_ACCOMMODATIONS = 2
    accommodation = accommodation_repository.list_all(per_page=2)
    assert len(accommodation) == TOTAL_ACCOMMODATIONS


def test_list_all_out_range_return_0(accommodation_repository):
    TOTAL_ACCOMMODATIONS = 0
    accommodation = accommodation_repository.list_all(page=60, per_page=1)
    assert len(accommodation) == TOTAL_ACCOMMODATIONS


def test_not_found_accommodation_by_id(accommodation_repository):
    existing = accommodation_repository.find_by_id(
        '01JA5EZ0BBQRGDX69PNTVG3N5E'
    )

    assert not existing


def test_find_accommodation_by_id(accommodation_repository):
    accommodation = accommodation_repository.find_by_id(
        '01JAFQXR26049VNR64PJE3J1W4'
    )
    assert accommodation


def test_not_found_accommodation_by_name(accommodation_repository):
    existing = accommodation_repository.find_by_name('Luxur')
    assert not existing


def test_find_accommodation_by_name(accommodation_repository):
    accommodation = accommodation_repository.find_by_name('Luxury Penthouse')
    assert accommodation


def test_create_accommodation(accommodation_repository, session):
    dto = AccommodationCreateDTO(
        name='Teste Acomodação',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=120,
        amenities=[],
    )

    accommodation = Accommodation.create(dto)

    assert not accommodation.ulid

    accommodation_repository.create(accommodation)

    accommodation_created = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == accommodation.name
        )
    )
    assert accommodation_created is not None


def test_create_2_accommodation_in_a_row(accommodation_repository, session):
    dto = AccommodationCreateDTO(
        name='Teste Acomodação',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=120,
        amenities=[],
    )

    dto2 = AccommodationCreateDTO(
        name='Teste Acomodação 2',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=120,
        amenities=[],
    )

    accommodation = Accommodation.create(dto)
    accommodation2 = Accommodation.create(dto2)

    assert not accommodation.ulid
    assert not accommodation2.ulid

    accommodation_repository.create(accommodation)
    accommodation_repository.create(accommodation2)

    created_accommodation = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == accommodation.name
        )
    )

    created_accommodation2 = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == accommodation2.name
        )
    )
    assert created_accommodation is not None
    assert created_accommodation2 is not None


def test_update_accommodation_name(accommodation_repository, session):
    existing_db_accommodation = session.get_one(
        AccommodationDB, '01JAFQXR26049VNR64PJE3J1W4'
    )

    accommodation = Accommodation.from_db(existing_db_accommodation)

    accommodation.name = 'Super Acomodação Teste'

    updated_accommodation = accommodation_repository.update(accommodation)

    assert updated_accommodation.name == 'Super Acomodação Teste'


def test_update_accommodation_amenities(accommodation_repository, session):
    TOTAL_AMENITIES = 3
    existing_db_accommodation = session.get_one(
        AccommodationDB, '01JAFQXR26049VNR64PJE3J1W4'
    )

    accommodation = Accommodation.from_db(existing_db_accommodation)

    accommodation.amenities = [
        Amenitie(name='WiFi'),
        Amenitie(name='Toalhas'),
        Amenitie(name='Ducha'),
    ]

    updated_accommodation = accommodation_repository.update(accommodation)

    assert updated_accommodation.amenities[0].name == 'WiFi'
    assert len(updated_accommodation.amenities) == TOTAL_AMENITIES


def test_delete_accommodation(accommodation_repository):
    accommodation_repository.delete('01JAFQXR26049VNR64PJE3J1W4')

    with pytest.raises(NoResultFound):
        accommodation_repository.delete('01JAFQXR26049VNR64PJE3J1W4')
