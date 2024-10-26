from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.database.models import AccommodationDB, BookingDB, GuestDB
from app.entities.Accommodation import Accommodation
from app.entities.Booking import Booking, BookingCreateDTO, BookingUpdateDTO
from app.entities.Guest import Guest
from app.schemas.Enums import BookingStatus


@pytest.fixture()
def booking_repository(repository_factory):
    booking_repository = repository_factory.create_booking_respository()
    return booking_repository


def test_list_all_bookings(booking_repository):
    TOTAL_BOOKINGS = 5
    bookings = booking_repository.list_all()
    assert len(bookings) == TOTAL_BOOKINGS


def test_list_all_bookings_20_per_page(booking_repository):
    TOTAL_BOOKINGS = 2
    bookings = booking_repository.list_all(per_page=2)
    assert len(bookings) == TOTAL_BOOKINGS


def test_list_all_out_range_return_0(booking_repository):
    TOTAL_BOOKINGS = 0
    bookings = booking_repository.list_all(page=60, per_page=1)
    assert len(bookings) == TOTAL_BOOKINGS


def test_not_found_booking_by_id(booking_repository):
    existing = booking_repository.find_by_id('01JA5EZ0BBQRGDX69PNTVG3N5E')
    assert not existing


def test_find_booking_by_id(booking_repository):
    booking = booking_repository.find_by_id('01JB3HNXD570W7V12DSQWS2XMJ')
    assert booking


def test_create_booking(booking_repository, session):
    dto = BookingCreateDTO(
        check_in=datetime(2024, 10, 20),
        check_out=datetime(2024, 10, 25),
        guest_document='1234325',
        accommodation_ulid='01JAFQXR26049VNR64PJE3J1W4',
    )

    db_guest = session.get_one(GuestDB, '01JB3HNWQ2D7XPPJ181G3YTH8T')
    db_accommodation = session.get_one(
        AccommodationDB, '01JAFQXR26049VNR64PJE3J1W4'
    )

    booking = Booking.create(
        dto,
        guest=Guest.from_db(db_guest),
        accommodation=Accommodation.from_db(db_accommodation),
    )

    booking_repository.create(booking)

    booking_created = session.scalar(
        select(BookingDB).where(BookingDB.locator == booking.locator)
    )
    assert booking_created is not None
    assert booking_created.check_in == booking.check_in
    assert booking_created.check_out == booking.check_out


def test_update_booking(booking_repository):
    update_data = BookingUpdateDTO(
        check_in=datetime(2024, 10, 20), check_out=datetime(2024, 10, 25)
    )

    updated_booking = booking_repository.update(
        '01JB3HNXD570W7V12DSQWS2XMJ', update_data
    )

    assert updated_booking.check_in == update_data.check_in
    assert updated_booking.check_out == update_data.check_out


def test_update_status_booking(booking_repository):
    new_status = BookingStatus.ACTIVE
    updated_booking = booking_repository.update_status(
        '01JB3HNXD570W7V12DSQWS2XMJ', new_status
    )

    assert updated_booking.status == new_status.value


def test_delete_booking(booking_repository):
    booking_repository.delete('01JB3HNXD570W7V12DSQWS2XMJ')

    with pytest.raises(NoResultFound):
        booking_repository.delete('01JB3HNXD570W7V12DSQWS2XMJ')


@pytest.mark.parametrize(
    ('check_in', 'check_out', 'expected_result'),
    [
        # Testes sem conflito
        (
            datetime(2023, 5, 11),
            datetime(2023, 5, 20),
            False,
        ),  # Fora do período da primeira reserva
        (
            datetime(2023, 6, 21),
            datetime(2023, 6, 25),
            False,
        ),  # Fora do período da segunda reserva
        (
            datetime(2024, 12, 16),
            datetime(2024, 12, 20),
            False,
        ),  # Fora do período da quinta reserva
        # Testes com conflito completo
        (
            datetime(2023, 5, 2),
            datetime(2023, 5, 5),
            True,
        ),  # Dentro da primeira reserva
        (
            datetime(2024, 12, 2),
            datetime(2024, 12, 14),
            True,
        ),  # Dentro da quinta reserva
        # Testes com conflito parcial
        (
            datetime(2023, 5, 9),
            datetime(2023, 5, 15),
            True,
        ),  # Sobreposição no final da primeira reserva
        (
            datetime(2023, 6, 14),
            datetime(2023, 6, 16),
            True,
        ),  # Sobreposição no início da segunda reserva
        (
            datetime(2024, 12, 10),
            datetime(2024, 12, 20),
            True,
        ),  # Sobreposição no final da quinta reserva
    ],
)
def test_conflicting_booking(
    booking_repository, check_in, check_out, expected_result
):
    conflict = booking_repository.is_in_conflict(check_in, check_out)
    assert conflict == expected_result
