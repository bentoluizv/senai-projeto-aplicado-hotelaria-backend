import pytest
from sqlalchemy.exc import NoResultFound

from app.database.models import AccommodationDB
from app.entities.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)


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
    with pytest.raises(NoResultFound):
        accommodation_repository.find_by_id('01JA5EZ0BBQRGDX69PNTVG3N5E')


def test_find_accommodation_by_id(accommodation_repository):
    accommodation = accommodation_repository.find_by_id(
        '01JAFQXR26049VNR64PJE3J1W4'
    )
    assert accommodation


def test_not_found_accommodation_by_name(accommodation_repository):
    with pytest.raises(NoResultFound):
        accommodation_repository.find_by_name('Luxur')


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

    accommodation_repository.create(accommodation)

    accommodation_created = session.get(
        AccommodationDB, str(accommodation.ulid)
    )
    assert accommodation_created is not None
    assert accommodation_created.ulid == str(accommodation.ulid)


def test_update_accommodation(accommodation_repository):
    update_data = AccommodationUpdateDTO(name='Super Acomodação Teste')

    updated_guest = accommodation_repository.update(
        '01JAFQXR26049VNR64PJE3J1W4', update_data
    )

    assert updated_guest.name == 'Super Acomodação Teste'


def test_delete_accommodation(accommodation_repository):
    accommodation_repository.delete('01JAFQY09Z7ABD18R5MHWTPWJS')

    with pytest.raises(NoResultFound):
        accommodation_repository.delete('01JAFQY09Z7ABD18R5MHWTPWJS')
