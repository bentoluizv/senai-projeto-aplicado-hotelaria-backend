from sqlalchemy import select

from app.infra.database.models import AmenitieDB
from app.schemas.Amenitie import AmenitieCreateDTO
from app.services.amenities import create


def test_create_amenitie(session):
    amenitie = AmenitieCreateDTO(name='banheira')
    create(session, amenitie)
    amenitie = session.scalar(
        select(AmenitieDB).where(AmenitieDB.name == amenitie.name)
    )
    assert amenitie.name == 'banheira'
