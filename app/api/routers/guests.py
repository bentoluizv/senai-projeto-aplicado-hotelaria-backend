from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_database_session
from app.database.models import GuestDB
from app.domain.Guest import Guest

router = APIRouter(tags=['Hóspedes'], prefix='/hospedes')


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Guest,
)
async def create_guest(
    guest: Guest, session: Session = Depends(get_database_session)
):
    db_guest = session.get(GuestDB, guest.document)

    if db_guest:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Guest already exists'
        )
    db_guest = GuestDB(
        uuid=guest.uuid,
        name=guest.name,
        document=guest.document,
        created_at=guest.created_at,
        surname=guest.surname,
        country=guest.country,
        phone=guest.phone,
    )

    session.add(db_guest)
    session.commit()

    return db_guest


@router.get('/', status_code=HTTPStatus.OK, response_model=list[Guest])
async def list_all_guests(session: Session = Depends(get_database_session)):
    db_guests = session.scalars(select(GuestDB)).all()
    return {'guests': db_guests}


@router.get(
    '/{document}',
    status_code=HTTPStatus.OK,
    response_model=Guest,
)
async def find_guest(
    document: str, session: Session = Depends(get_database_session)
):
    db_guest = session.get(GuestDB, document)

    if not db_guest:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Guest not found'
        )

    return db_guest


@router.put(
    '/{document}',
    status_code=HTTPStatus.OK,
    response_model=Guest,
)
async def update_guest(
    document: str,
    guest: Guest,
    session: Session = Depends(get_database_session),
):
    db_guest = session.get(GuestDB, document)

    if not db_guest:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Guest not found'
        )
    db_guest.name = guest.name
    db_guest.surname = guest.surname
    db_guest.document = guest.document
    db_guest.phone = guest.phone
    db_guest.country = guest.country

    session.commit()
    session.refresh(db_guest)

    return db_guest


@router.delete('/{document}', status_code=HTTPStatus.NO_CONTENT)
async def delete_guest(
    document: str, session: Session = Depends(get_database_session)
):
    db_guest = session.get(GuestDB, document)

    if not db_guest:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Guest not found'
        )
    session.delete(db_guest)
    session.commit()
