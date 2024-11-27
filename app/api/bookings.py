from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.BookingController import BookingController
from app.entities.Booking import Booking, BookingCreateDTO, BookingUpdateDTO
from app.entities.schemas.ListSettings import (
    ListFilter,
    ListSettings,
    Pagination,
)
from app.entities.schemas.Message import Message

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
    dependencies=[],
)

BookingController = Annotated[BookingController, Depends(BookingController)]


class BookingList(BaseModel):
    bookings: list[Booking]


@router.get('/', response_model=BookingList, status_code=HTTPStatus.OK)
def list_all_bookings(
    booking_controller: BookingController,  # type: ignore
    check_in: datetime | None = None,
    check_out: datetime | None = None,
    page: int = 1,
    per_page: int = 10,
):
    if check_in and check_out:
        settings = ListSettings(
            pagination=Pagination(page=page, per_page=per_page),
            filter=ListFilter(check_in=check_in, check_out=check_out),
        )
        bookings = booking_controller.list_all(settings)
        return BookingList(bookings=bookings)

    settings = ListSettings(
        pagination=Pagination(page=page, per_page=per_page),
    )
    bookings = booking_controller.list_all(settings)
    return BookingList(bookings=bookings)


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=Booking)
def find_by_id(booking_controller: BookingController, id: str):  # type: ignore
    booking = booking_controller.find_by_id(id)
    return booking


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Booking,
)
def create_new_booking(
    data: BookingCreateDTO,
    booking_controller: BookingController,  # type: ignore
):
    booking = booking_controller.create(data)
    return booking


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def update_booking(
    data: BookingUpdateDTO,
    booking_controller: BookingController,  # type: ignore
    id: str,
):
    booking_controller.update(id, data)
    return Message(message='UPDATED')


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_booking(
    booking_controller: BookingController,  # type: ignore
    id: str,
):
    booking_controller.delete(id)
    return Message(message='DELETED')
