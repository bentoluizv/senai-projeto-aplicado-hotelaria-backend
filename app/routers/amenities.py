from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.database.db import get_database_session
from app.infra.database.models import AmenitieDB

router = APIRouter(tags=['Amenidades'], prefix='/amenities')


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=list[AmenitieDB],
)
async def list_all_amenities(
    session: Session = Depends(get_database_session),
): ...
