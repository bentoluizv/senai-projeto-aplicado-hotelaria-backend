from sqlalchemy import select

from app.infra.database.models import AmenitieDB
from app.schemas.Amenitie import AmenitieCreateDTO


def test_create_new_amenitie(repository_factory, session):
    amenitie_repository = repository_factory.create_amenitie_repository()
    dto = AmenitieCreateDTO(name='banheira')
    amenitie_repository.create(dto)
    amenitie = session = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == dto.name)
    )
    assert amenitie


def test_list_all_guests(repository_factory):
    repository = repository_factory.create_guest_repository()
    guests = repository.list_all()
    assert len(guests) == 1
