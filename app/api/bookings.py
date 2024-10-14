from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.BookingController import BookingController
from app.entities.Booking import Booking

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
    page: int = 1,
    per_page: int = 10,
):
    bookings = booking_controller.list_all(page=page, per_page=per_page)
    return BookingList(bookings=bookings)


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=Booking)
def find_by_id(booking_controller: BookingController, id: str):  # type: ignore
    booking = booking_controller.find_by_id(id)
    return booking
