import pytest
from sqlalchemy import select

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import AccommodationDB
from app.schemas.Accommodation import (
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.services.accommodations import (
    create,
    delete,
    find_by_id,
    list_all,
    update,
)


def test_create_accommodation(session):
    new_accommodation = AccommodationCreateDTO(
        name='Quarto Individual',
        status='Disponivel',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=350,
        amenities=[],
    )
    create(session, new_accommodation)

    exists = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == new_accommodation.name
        )
    )

    assert exists


def test_create_accommodation_that_already_exists_should_raise(session):
    new_accommodation = AccommodationCreateDTO(
        name='Quarto de Teste',
        status='Disponivel',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=350,
        amenities=[],
    )

    with pytest.raises(AlreadyExistsError):
        create(session, new_accommodation)


def test_list_all_accommodations(session):
    accommodations = list_all(session)
    assert len(accommodations) == 1
    assert accommodations[0].name == 'Quarto de Teste'


def test_find_accommodation_by_id(session):
    accommodation = find_by_id(session, '1')
    assert accommodation
    assert accommodation.name == 'Quarto de Teste'


def test_find_accommodation_by_id_that_not_exists_should_raise(session):
    with pytest.raises(NotFoundError):
        find_by_id(session, '2')


def test_update_accommodation(session):
    data_to_update = AccommodationUpdateDTO(name='Quarto Teste 2')
    updated_accommodation = update(session, '1', data_to_update)
    existing_accommodation = session.scalar(
        select(AccommodationDB).where(AccommodationDB.name == 'Quarto Teste 2')
    )
    assert existing_accommodation is updated_accommodation


def test_delete_accommodation(session):
    delete(session, '1')

    with pytest.raises(NotFoundError):
        delete(session, '1')
