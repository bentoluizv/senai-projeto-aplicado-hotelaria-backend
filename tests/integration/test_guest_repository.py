from uuid import UUID

import pytest

from app.domain.errors.NotFoundError import NotFoundError
from app.domain.Guest import GuestCreateDTO, GuestUpdateDTO


def test_should_create_a_new_guest(repository_factory):
    TOTAL_GUESTS = 2
    guest_data = {
        'document': '22244455534',
        'name': 'Teste',
        'surname': 'Testamdp',
        'phone': '4895434521',
        'country': 'Brasil',
    }
    new_guest = GuestCreateDTO(**guest_data)
    repository = repository_factory.create_guest_repository()
    repository.insert(new_guest)

    all_guests = repository.list()
    assert len(all_guests) == TOTAL_GUESTS


def test_select_all_guests(repository_factory):
    repository = repository_factory.create_guest_repository()
    all_guests = repository.list()

    assert len(all_guests) == 1


def test_find_guest_by_id(repository_factory):
    repository = repository_factory.create_guest_repository()
    guest = repository.find_by_id(UUID('f20c129f-6b7e-4047-9f1c-63e52633c22e'))

    assert guest.name == 'Bento'


def test_update_guest(repository_factory):
    repository = repository_factory.create_guest_repository()
    repository.update(
        UUID('f20c129f-6b7e-4047-9f1c-63e52633c22e'),
        GuestUpdateDTO(name='Luiz'),
    )

    guest = repository.find_by_id(UUID('f20c129f-6b7e-4047-9f1c-63e52633c22e'))

    assert guest.name == 'Luiz'


def test_delete_guest(repository_factory):
    repository = repository_factory.create_guest_repository()
    repository.delete(UUID('f20c129f-6b7e-4047-9f1c-63e52633c22e'))

    with pytest.raises(NotFoundError):
        repository.find_by_id(UUID('f20c129f-6b7e-4047-9f1c-63e52633c22e'))
