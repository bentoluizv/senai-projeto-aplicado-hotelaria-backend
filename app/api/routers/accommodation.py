import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_database_session
from app.database.models import AccommodationDB, AmenitieDB
from app.domain.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)

router = APIRouter(tags=['Acomodações'], prefix='/acomodacoes')


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Accommodation,
)
async def create_accommodation(
    accommodation_dto: AccommodationCreateDTO,
    session: Session = Depends(get_database_session),
):
    db_accommodation = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.name == accommodation_dto.name
        )
    )

    if db_accommodation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Accommodation already exists',
        )

    db_amenities: List[AmenitieDB] = []

    for amenitie in accommodation_dto.amenities:
        db_amenitie = session.scalar(
            select(AmenitieDB).where(AmenitieDB.name == amenitie)
        )

        if db_amenitie:
            db_amenities.append(db_amenitie)

    db_accommodation = AccommodationDB(
        name=accommodation_dto.name,
        status=accommodation_dto.status,
        created_at=datetime.datetime.now(),
        single_beds=accommodation_dto.single_beds,
        double_beds=accommodation_dto.double_beds,
        min_nights=accommodation_dto.min_nights,
        total_guests=accommodation_dto.total_guests,
        price=accommodation_dto.price,
        amenities=db_amenities,
    )

    session.add(db_accommodation)
    session.commit()
    session.refresh(db_accommodation)
    return db_accommodation


@router.get('/', status_code=HTTPStatus.OK, response_model=list[Accommodation])
async def list_all_accommodations(
    session: Session = Depends(get_database_session),
):
    db_accommodations = session.scalars(select(AccommodationDB)).all()
    return {'accommodations': db_accommodations}


@router.get(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=Accommodation,
)
async def find_accommodation(
    id: str, session: Session = Depends(get_database_session)
):
    db_accommodation = session.get(AccommodationDB, id)

    if not db_accommodation:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Accommodation not found'
        )

    return db_accommodation


# TODO: Repensar Lógica de Update!! Objeto vem só com a propriedade a ser
#       atualizada e não todas.
@router.put(
    '/{id}',
    status_code=HTTPStatus.OK,
    response_model=Accommodation,
)
async def update_accommodation(
    id: str,
    accommodation_dto: AccommodationUpdateDTO,
    session: Session = Depends(get_database_session),
):
    db_accommodation = session.get(AccommodationDB, id)

    if not db_accommodation:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Accomodation not found'
        )

    # db_accommodation.name = accommodation_dto.name
    # db_accommodation.status = accommodation_dto.status
    # db_accommodation.total_guests = accommodation_dto.total_guests
    # db_accommodation.single_beds = accommodation_dto.single_beds
    # db_accommodation.double_beds = accommodation_dto.double_beds
    # db_accommodation.min_nights = accommodation_dto.min_nights
    # db_accommodation.price = accommodation_dto.price

    db_amenities: List[AmenitieDB] = []

    # for amenitie in accommodation_dto.amenities:
    #     db_amenitie = session.scalar(
    #         select(AmenitieDB).where(AmenitieDB.name == amenitie)
    #     )

    # if db_amenitie:
    #     db_amenities.append(db_amenitie)

    db_accommodation.amenities = db_amenities

    session.commit()
    session.refresh(db_accommodation)
    return db_accommodation


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_accommodation(
    id: int, session: Session = Depends(get_database_session)
):
    db_accommodations = session.get(AccommodationDB, id)

    if not db_accommodations:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Acommodation not found'
        )
    session.delete(db_accommodations)
    session.commit()
