from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.db import get_database_session
from app.infra.models import AmenitieDB
from app.schemas.Amenitie import AmenitieCreateDTO
from app.schemas.Message import Message

router = APIRouter(tags=['Amenidades'], prefix='/amenities')


@router.get('/', status_code=HTTPStatus.OK, response_model=list[AmenitieDB])
async def list_all_amenities(
    session: Annotated[Session, Depends(get_database_session)],
): ...


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_amenitie(
    new_amenitie: AmenitieCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
): ...
