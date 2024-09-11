from sqlalchemy import select

from app.infra.database.models import AmenitieDB
from app.schemas.Amenitie import AmenitieCreateDTO
from app.services.amenities import create, list_all


def test_create_amenitie(session):
    amenitie = AmenitieCreateDTO(name='banheira')
    create(session, amenitie)
    amenitie = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
    )
    assert amenitie.name == 'banheira'


def test_list_all_amenities(session):
    TOTAL_AMENITIES = 2
    amenities = list_all(session)
    assert len(amenities) == TOTAL_AMENITIES
    assert amenities[0].name == 'wifi'
