from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.errors.AlreadyExistsError import AlreadyExistsError
from app.infra.database.db import get_database_session
from app.infra.database.models import AmenitieDB
from app.schemas.Amenitie import AmenitieCreateDTO
from app.schemas.Message import Message
from app.services.amenities import (
    create,
    list_all,
)

router = APIRouter(tags=['Amenidades'], prefix='/amenities')


@router.get('/', status_code=HTTPStatus.OK, response_model=list[AmenitieDB])
async def list_all_amenities(
    session: Annotated[Session, Depends(get_database_session)],
):
    amenities = list_all(session)

    return amenities


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_amenitie(
    new_amenitie: AmenitieCreateDTO,
    session: Annotated[Session, Depends(get_database_session)],
):
    try:
        create(session, new_amenitie)
        return Message(content='CREATED')

    except AlreadyExistsError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=err.message
        )
