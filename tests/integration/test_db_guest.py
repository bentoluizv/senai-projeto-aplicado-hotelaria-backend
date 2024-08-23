import datetime
from uuid import uuid4

import pytest
from sqlalchemy import select, update

from app.database.models import GuestDB


@pytest.mark.skip()
def test_create_guest(session):
    new_guest = GuestDB(
        uuid=uuid4(),
        document='00157624242',
        created_at=datetime.datetime.now(),
        name='Bento Luiz',
        surname='Machado',
        country='Brasil',
        phone='48992054211',
    )
    session.add(new_guest)
    session.commit()

    guest = session.scalar(select(GuestDB).where(GuestDB.name == 'Bento Luiz'))
    assert guest.name == 'Bento Luiz'


@pytest.mark.skip()
def test_select_all_guests(session):
    TOTAL_GUESTS = 5
    statement = select(GuestDB)
    guest_db = session.scalars(statement).all()
    assert len(guest_db) == TOTAL_GUESTS


@pytest.mark.skip()
def test_find_guest_by_name(session):
    statement = select(GuestDB).where(GuestDB.name == 'Maria')
    guest_db = session.scalar(statement)
    assert guest_db
    assert guest_db.surname == 'Oliveira'


@pytest.mark.skip()
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


@pytest.mark.skip()
def test_delete_guest(session):
    guest_db = session.get(GuestDB, '98765432100')
    session.delete(guest_db)

    statement = select(GuestDB).where(GuestDB.name == 'Maria')
    exists = session.scalar(statement)
    assert not exists
