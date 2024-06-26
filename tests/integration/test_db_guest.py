import datetime

from sqlalchemy import select, update

from app.database.models import GuestDB


def test_create_guest(session):
    new_guest = GuestDB(
        document='00157624242',
        created_at=datetime.datetime.now().isoformat(),
        name='Bento Luiz',
        surname='Machado',
        country='Brasil',
        phone='48992054211',
    )
    session.add(new_guest)
    session.commit()

    guest = session.scalar(select(GuestDB).where(GuestDB.name == 'Bento Luiz'))
    assert guest.name == 'Bento Luiz'


def test_select_all_guests(session):
    TOTAL_GUESTS = 5
    statement = select(GuestDB)
    guest_db = session.scalars(statement).all()
    assert len(guest_db) == TOTAL_GUESTS


def test_find_guest_by_name(session):
    statement = select(GuestDB).where(GuestDB.name == 'Maria')
    guest_db = session.scalar(statement)
    assert guest_db
    assert guest_db.surname == 'Oliveira'


def test_update_guest(session):
    update_statement = (
        update(GuestDB)
        .where(GuestDB.name == 'Maria')
        .values(country='Argentina')
    )
    session.execute(update_statement)

    select_statement = select(GuestDB).where(GuestDB.name == 'Maria')
    guest_db = session.scalar(select_statement)
    assert guest_db
    assert guest_db.country == 'Argentina'


def test_delete_guest(session):
    guest_db = session.get(GuestDB, '98765432100')
    session.delete(guest_db)

    statement = select(GuestDB).where(GuestDB.name == 'Maria')
    exists = session.scalar(statement)
    assert not exists
