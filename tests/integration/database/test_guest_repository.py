from sqlalchemy import select

from app.infra.database.models import GuestDB
from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO


def test_create_new_guest(repository_factory, session):
    guest_repository = repository_factory.create_guest_repository()
    dto = GuestCreateDTO(
        document='31578421514',
        name='Astrubal',
        surname='Lima',
        phone='48923568741',
        country='Brasil',
    )
    guest_repository.create(dto)
    guest = session.scalar(select(GuestDB).where(GuestDB.name == dto.name))
    assert guest


def test_find_guest_by_id(repository_factory):
    repository = repository_factory.create_guest_repository()
    guest = repository.find_by_id('01J9V645ZGN1JMCEFT9WVKQGBC')
    assert guest.name == 'Bento'


def test_list_all_guests(repository_factory):
    repository = repository_factory.create_guest_repository()
    guests = repository.list_all()
    assert len(guests) == 1


def test_update_guest(repository_factory, session):
    repository = repository_factory.create_guest_repository()
    dto = GuestUpdateDTO(phone='48974521254')
    repository.update('01J9V645ZGN1JMCEFT9WVKQGBC', dto)
    db_guest = session.get(GuestDB, '01J9V645ZGN1JMCEFT9WVKQGBC')
    assert db_guest.phone == '48974521254'


def test_delete_guest(repository_factory, session):
    repository = repository_factory.create_guest_repository()
    repository.delete('01J9V645ZGN1JMCEFT9WVKQGBC')
    guest = session.get(GuestDB, '01J9V645ZGN1JMCEFT9WVKQGBC')

    assert not guest
