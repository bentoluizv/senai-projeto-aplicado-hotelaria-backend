from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.database.models import BookingDB, BookingStatus
from app.entities.Accommodation import Accommodation
from app.entities.Booking import Booking, BookingCreateDTO, BookingUpdateDTO
from app.entities.Guest import Guest


@pytest.fixture()
def booking_repository(repository_factory):
    booking_repository = repository_factory.create_booking_respository()
    return booking_repository


def test_list_all_bookings(booking_repository):
    TOTAL_BOOKINGS = 10
    bookings = booking_repository.list_all()
    assert len(bookings) == TOTAL_BOOKINGS


def test_list_all_bookings_20_per_page(booking_repository):
    TOTAL_BOOKINGS = 20
    bookings = booking_repository.list_all(per_page=20)
    assert len(bookings) == TOTAL_BOOKINGS


def test_list_all_out_range_return_0(booking_repository):
    TOTAL_BOOKINGS = 0
    bookings = booking_repository.list_all(page=60, per_page=5)
    assert len(bookings) == TOTAL_BOOKINGS


def test_not_found_booking_by_id(booking_repository):
    with pytest.raises(NoResultFound):
        booking_repository.find_by_id('01JA5EZ0BBQRGDX69PNTVG3N5E')


def test_find_booking_by_id(booking_repository, db_booking):
    booking = booking_repository.find_by_id('01JA5EZ0BBQRGDX69PNTVG3N5E')
    assert booking


def test_create_booking(
    booking_repository, session, db_guest, db_accommodation
):
    dto = BookingCreateDTO(
        check_in=datetime(2024, 10, 20),
        check_out=datetime(2024, 10, 25),
        guest_document=db_guest.document,
        accommodation_ulid=db_accommodation.ulid,
    )

    booking = Booking.create(
        dto,
        guest=Guest.from_db(db_guest),
        accommodation=Accommodation.from_db(db_accommodation),
    )

    booking_repository.create(booking)

    booking_created = session.scalar(
        select(BookingDB).where(BookingDB.ulid == str(booking.ulid))
    )
    assert booking_created is not None
    assert booking_created.ulid == str(booking.ulid)
    assert booking_created.check_in == booking.check_in
    assert booking_created.check_out == booking.check_out


def test_update_booking(booking_repository, db_booking):
    update_data = BookingUpdateDTO(
        check_in=datetime(2024, 10, 20), check_out=datetime(2024, 10, 25)
    )

    updated_booking = booking_repository.update(
        str(db_booking.ulid), update_data
    )

    assert updated_booking.check_in == update_data.check_in
    assert updated_booking.check_out == update_data.check_out


def test_update_status_booking(booking_repository, db_booking):
    new_status = BookingStatus.ACTIVE
    updated_booking = booking_repository.update_status(
        str(db_booking.ulid), new_status
    )

    assert updated_booking.status == new_status


@pytest.mark.skip()
def test_delete_booking(booking_repository, db_booking, session):
    booking_repository.delete(str(db_booking.ulid))

    # Verifica se a reserva foi deletada
    deleted_booking = (
        session.query(BookingDB)
        .filter_by(ulid=str(db_booking.ulid))
        .one_or_none()
    )
    assert deleted_booking is None


@pytest.mark.skip()
def test_conflicting_booking_true(booking_repository, db_booking):
    # Teste para verificar conflito de datas
    conflict = booking_repository.is_in_conflict(
        db_booking.check_in, db_booking.check_out
    )
    assert conflict is True


@pytest.mark.skip()
def test_conflicting_booking_false(booking_repository):
    # Teste para verificar que não há conflito quando datas não colidem
    no_conflict = booking_repository.is_in_conflict(
        datetime(2025, 1, 1), datetime(2025, 1, 10)
    )
    assert no_conflict is False
