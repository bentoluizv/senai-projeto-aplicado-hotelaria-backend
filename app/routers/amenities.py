from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data.database.db import get_database_session
from app.domain.Amenitie import Amenitie

router = APIRouter(tags=['Amenidades'], prefix='/amenities')


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=list[Amenitie],
)
async def list_all_amenities(
    session: Session = Depends(get_database_session),
): ...
