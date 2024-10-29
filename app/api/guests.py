from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.GuestController import GuestController
from app.entities.Guest import Guest, GuestCreateDTO, GuestUpdateDTO
from app.schemas.Message import Message
from app.utils.is_ulid import is_ulid

router = APIRouter(
    prefix='/guests',
    tags=['Guests'],
    dependencies=[],
)

GuestController = Annotated[GuestController, Depends(GuestController)]


class GuestList(BaseModel):
    guests: list[Guest]


@router.get('/', response_model=GuestList, status_code=HTTPStatus.OK)
def list_all_guests(
    guest_controller: GuestController,  # type: ignore
    page: int = 1,
    per_page: int = 10,
):
    guests = guest_controller.list_all(page=page, per_page=per_page)
    return GuestList(guests=guests)


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=Guest)
def find_by_id(guest_controller: GuestController, id: str):  # type: ignore
    if is_ulid(id):
        guest = guest_controller.find_by_id(id)
        return guest

    else:
        guest = guest_controller.find_by_document(id)
        return guest


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
def create_new_guests(
    data: GuestCreateDTO,
    guest_controller: GuestController,  # type: ignore
):
    guest_controller.create(data)
    return Message(message='CREATED')


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def update_guests(
    data: GuestUpdateDTO,
    guest_controller: GuestController,  # type: ignore
    id: str,
):
    guest_controller.update(id, data)
    return Message(message='UPDATED')


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_guests(
    guest_controller: GuestController,  # type: ignore
    id: str,
):
    guest_controller.delete(id)
    return Message(message='DELETED')
