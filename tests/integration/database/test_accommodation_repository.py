from sqlalchemy import select

from app.infra.database.models import AccommodationDB
from app.schemas.Accommodation import (
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)


def test_create_accommodation(repository_factory, session):
    repository = repository_factory.create_accommodation_repository()
    new_accommodation = AccommodationCreateDTO(
        name='Quarto Individual',
        status='Disponivel',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=350,
        amenities=[],
    )
    repository.create(new_accommodation)

    db_accommodation = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == new_accommodation.name
        )
    )

    assert db_accommodation


def test_list_all_accommodations(repository_factory):
    repository = repository_factory.create_accommodation_repository()
    accommodations = repository.list_all()
    assert len(accommodations) == 1
    assert accommodations[0].name == 'Quarto de Teste'


def test_find_accommodation_by_id(repository_factory):
    repository = repository_factory.create_accommodation_repository()
    accommodation = repository.find_by_id('01J9V65AWQ1ME0J2SCYBD5S8B1')
    assert accommodation
    assert accommodation.name == 'Quarto de Teste'


def test_update_accommodation(repository_factory, session):
    repository = repository_factory.create_accommodation_repository()
    data_to_update = AccommodationUpdateDTO(name='Quarto Teste 2')
    repository.update('01J9V65AWQ1ME0J2SCYBD5S8B1', data_to_update)

    db_accommodation = session.scalar(
        select(AccommodationDB).where(AccommodationDB.name == 'Quarto Teste 2')
    )

    assert db_accommodation


def test_delete_accommodation(repository_factory, session):
    repository = repository_factory.create_accommodation_repository()
    repository.delete('01J9V65AWQ1ME0J2SCYBD5S8B1')
    session.get(AccommodationDB, '01J9V65AWQ1ME0J2SCYBD5S8B1')
