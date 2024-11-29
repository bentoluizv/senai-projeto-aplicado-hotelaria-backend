from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.BookingController import BookingController
from app.controller.GuestController import GuestController
from app.entities.Booking import Booking
from app.entities.Guest import Guest, GuestCreateDTO, GuestUpdateDTO
from app.entities.schemas.ListSettings import ListSettings, Pagination
from app.entities.schemas.Message import Message
from app.utils.is_ulid import is_ulid

router = APIRouter(
    prefix='/guests',
    tags=['Guests'],
    dependencies=[],
)

GuestController = Annotated[GuestController, Depends(GuestController)]
BookingController = Annotated[BookingController, Depends(BookingController)]


class GuestList(BaseModel):
    guests: list[Guest]


class BookingList(BaseModel):
    bookings: list[Booking]


@router.get('/', response_model=GuestList, status_code=HTTPStatus.OK)
def list_all_guests(
    guest_controller: GuestController,  # type: ignore
    page: int = 1,
    per_page: int = 10,
):
    guests = guest_controller.list_all(page=page, per_page=per_page)
    return GuestList(guests=guests)


@router.get(
    '/{ulid}/reservas', response_model=BookingList, status_code=HTTPStatus.OK
)
def list_all_bookings_by_guest(
    booking_controller: BookingController,  # type: ignore
    ulid: str,
    page: int = 1,
    per_page: int = 10,
):
    settings = ListSettings(
        pagination=Pagination(page=page, per_page=per_page),
    )
    bookings = booking_controller.list_all_by_guest(settings, ulid)
    return BookingList(bookings=bookings)


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
def update_guest(
    data: GuestUpdateDTO,
    guest_controller: GuestController,  # type: ignore
    id: str,
):
    guest_controller.update(id, data)
    return Message(message='UPDATED')


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_guest(
    guest_controller: GuestController,  # type: ignore
    id: str,
):
    guest_controller.delete(id)
    return Message(message='DELETED')
