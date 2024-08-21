from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_database_session
from app.database.models import AmenitieDB
from app.domain.Amenitie import AmenitieList

router = APIRouter(tags=['Amenidades'], prefix='/amenities')


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=AmenitieList,
)
async def list_all_amenities(session: Session = Depends(get_database_session)):
    db_amenities = session.scalars(select(AmenitieDB)).all()
    return {'amenities': db_amenities}
