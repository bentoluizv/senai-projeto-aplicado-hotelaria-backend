import pytest


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
