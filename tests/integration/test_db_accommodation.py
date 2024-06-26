import datetime

from sqlalchemy import select, update

from app.database.models import AccommodationDB, AmenitieDB


def test_create_accommodation(session):
    new_accommodation = AccommodationDB(
        name='Quarto Individual',
        created_at=datetime.datetime.now().isoformat(),
        status='Disponivel',
        single_beds=1,
        total_guests=0,
        double_beds=0,
        min_nights=2,
        price=180,
        amenities=[],
    )

    wifiAmenitie = session.get(AmenitieDB, 2)
    if wifiAmenitie:
        new_accommodation.amenities.append(wifiAmenitie)

    session.add(new_accommodation)
    session.commit()

    accommodation = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == 'Quarto Individual'
        )
    )
    assert accommodation.amenities[0].name == 'wifi'


def test_select_all_accommodations(session):
    TOTAL_ACCOMMODATION = 6
    statement = select(AccommodationDB)
    accommodation_db = session.scalars(statement).all()
    assert len(accommodation_db) == TOTAL_ACCOMMODATION


def test_find_accommodation_by_name(session):
    ACCOMMODATION_PRICE = 590
    statement = select(AccommodationDB).where(AccommodationDB.name == 'Domo')
    accommodation_db = session.scalar(statement)
    assert accommodation_db
    assert accommodation_db.price == ACCOMMODATION_PRICE


def test_update_accommodation(session):
    statement = (
        update(AccommodationDB)
        .where(AccommodationDB.name == 'Domo')
        .values(price=1800)
    )
    session.execute(statement)

    statement = select(AccommodationDB).where(AccommodationDB.name == 'Domo')
    ACCOMMODATION_PRICE = 1800
    accommodation_db = session.scalar(statement)
    assert accommodation_db
    assert accommodation_db.price == ACCOMMODATION_PRICE


def test_delete_accommodation(session):
    accommodation_db = session.get(AccommodationDB, 1)
    session.delete(accommodation_db)

    statement = select(AccommodationDB).where(AccommodationDB.name == 'Domo')
    exists = session.scalar(statement)
    assert not exists
