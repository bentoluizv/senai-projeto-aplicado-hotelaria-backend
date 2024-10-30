from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.AccommodationController import AccommodationController
from app.entities.Accommodation import (
    Accommodation,
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)
from app.entities.schemas.Message import Message

router = APIRouter(
    prefix='/accommodations',
    tags=['Accommodation'],
    dependencies=[],
)

AccommodationController = Annotated[
    AccommodationController, Depends(AccommodationController)
]


class AccommodationList(BaseModel):
    accommodations: list[Accommodation]


@router.get('/', response_model=AccommodationList, status_code=HTTPStatus.OK)
def list_all_accommodations(
    accommodation_controller: AccommodationController,  # type: ignore
    page: int = 1,
    per_page: int = 10,
):
    accommodations = accommodation_controller.list_all(
        page=page, per_page=per_page
    )
    return AccommodationList(accommodations=accommodations)


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=Accommodation)
def find_accommodation_by_id(
    accommodation_controller: AccommodationController,  # type: ignore
    id: str,
):
    accommodation = accommodation_controller.find_by_id(id)
    return accommodation


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
def create_new_accommodation(
    data: AccommodationCreateDTO,
    accommodation_controller: AccommodationController,  # type: ignore
):
    accommodation_controller.create(data)
    return Message(message='CREATED')


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def update_accommodation(
    data: AccommodationUpdateDTO,
    accommodation_controller: AccommodationController,  # type: ignore
    id: str,
):
    accommodation_controller.update(id, data)
    return Message(message='UPDATED')


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_accommodation(
    accommodation_controller: AccommodationController,  # type: ignore
    id: str,
):
    accommodation_controller.delete(id)
    return Message(message='DELETED')
