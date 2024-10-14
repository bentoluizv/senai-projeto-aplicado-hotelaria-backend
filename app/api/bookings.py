from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_database_session
from app.database.repositories.BookingRepository import BookingRepository
from app.entities.Booking import Booking
from app.errors.OutOfRangeError import OutOfRangeError

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
    dependencies=[],
)


class BookingList(BaseModel):
    bookings: list[Booking]


@router.get('/', response_model=BookingList, status_code=HTTPStatus.OK)
def list_all_bookings(
    session: Annotated[Session, Depends(get_database_session)],
    page: int = 1,
    per_page: int = 10,
):
    try:
        booking_repository = BookingRepository(session)
        bookings = booking_repository.list_all(page=page, per_page=per_page)

        return BookingList(bookings=bookings)

    except OutOfRangeError as Error:
        raise Error
