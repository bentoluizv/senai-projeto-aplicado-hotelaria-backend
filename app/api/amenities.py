from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.AmenitieController import AmenitieController
from app.entities.Amenitie import Amenitie, AmenitieCreateDTO
from app.schemas.Message import Message

router = APIRouter(
    prefix='/amenities',
    tags=['Amenitie'],
    dependencies=[],
)

AmenitieController = Annotated[AmenitieController, Depends(AmenitieController)]


class AmenitieList(BaseModel):
    amenities: list[Amenitie]


@router.get('/', response_model=AmenitieList, status_code=HTTPStatus.OK)
def list_all_amenities(
    amenitie_controller: AmenitieController,  # type: ignore
    page: int = 1,
    per_page: int = 10,
):
    amenities = amenitie_controller.list_all(page=page, per_page=per_page)
    return AmenitieList(amenities=amenities)


@router.get('/{name}', status_code=HTTPStatus.OK, response_model=Amenitie)
def find_amenitie_by_name(amenitie_controller: AmenitieController, name: str):  # type: ignore
    amenitie = amenitie_controller.find_by_name(name)
    return amenitie


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
def create_new_amenitie(
    data: AmenitieCreateDTO,
    amenitie_controller: AmenitieController,  # type: ignore
):
    amenitie_controller.create(data)
    return Message(message='CREATED')
