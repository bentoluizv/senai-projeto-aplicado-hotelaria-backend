from datetime import datetime
from http import HTTPStatus

import pytest

from app.entities.Booking import BookingCreateDTO, BookingUpdateDTO


def test_list_all_bookings(client):
    TOTAL_BOOKINGS = 5
    response = client.get('/bookings/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'bookings' in response.json()
    assert len(response.json()['bookings']) == TOTAL_BOOKINGS


def test_list_all_bookings_20_per_page(client):
    TOTAL_BOOKINGS = 2
    response = client.get('/bookings/?page=1&per_page=2')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'bookings' in response.json()
    assert len(response.json()['bookings']) == TOTAL_BOOKINGS


def test_list_all_out_range(client):
    response = client.get('/bookings/?page=8&per_page=5')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert isinstance(response.json(), dict)
    assert 'detail' in response.json()
    assert (
        response.json()['detail']
        == 'Page 8 is out of range. There are only 1 pages.'
    )


def test_find_booking_by_id(client, db_booking):
    response = client.get(f'/bookings/{db_booking.ulid}')
    booking = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert booking['guest']
    assert booking['accommodation']
    assert booking['budget'] > 0


def test_not_found_booking_by_id(client):
    response = client.get('/bookings/01JA5EZ0BBQRGDX69PNTVG3N5E')
    booking = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json(), dict)
    assert (
        booking['detail']
        == """Booking with ID '01JA5EZ0BBQRGDX69PNTVG3N5E' not found."""
    )


@pytest.mark.parametrize(
    ('check_in', 'check_out', 'expected_status'),
    [
        # Testes sem conflito
        (
            datetime(2023, 5, 11),
            datetime(2023, 5, 20),
            HTTPStatus.CREATED,
        ),  # Fora do período da primeira reserva
        (
            datetime(2023, 6, 21),
            datetime(2023, 6, 25),
            HTTPStatus.CREATED,
        ),  # Fora do período da segunda reserva
        (
            datetime(2024, 12, 16),
            datetime(2024, 12, 20),
            HTTPStatus.CREATED,
        ),  # Fora do período da quinta reserva
        # Testes com conflito completo
        (
            datetime(2023, 5, 2),
            datetime(2023, 5, 5),
            HTTPStatus.CONFLICT,
        ),  # Dentro da primeira reserva
        (
            datetime(2024, 12, 2),
            datetime(2024, 12, 14),
            HTTPStatus.CONFLICT,
        ),  # Dentro da quinta reserva
        # Testes com conflito parcial
        (
            datetime(2023, 5, 9),
            datetime(2023, 5, 15),
            HTTPStatus.CONFLICT,
        ),  # Sobreposição no final da primeira reserva
        (
            datetime(2023, 6, 14),
            datetime(2023, 6, 16),
            HTTPStatus.CONFLICT,
        ),  # Sobreposição no início da segunda reserva
        (
            datetime(2024, 12, 10),
            datetime(2024, 12, 20),
            HTTPStatus.CONFLICT,
        ),  # Sobreposição no final da quinta reserva
    ],
)
def test_create_new_booking(  # noqa: PLR0913, PLR0917
    client, db_guest, db_accommodation, check_in, check_out, expected_status
):
    dto = BookingCreateDTO(
        check_in=check_in,
        check_out=check_out,
        guest_document=db_guest.document,
        accommodation_ulid=db_accommodation.ulid,
    )

    data = dto.model_dump_json()
    response = client.post('/bookings', data=data)
    assert response.status_code == expected_status


def test_update_booking(client, db_booking):
    dto = BookingUpdateDTO(
        check_in=datetime(2026, 1, 1),
        check_out=datetime(2026, 1, 12),
    )

    data = dto.model_dump_json()
    response = client.put(f'/bookings/{db_booking.ulid}', data=data)
    assert response.status_code == HTTPStatus.OK


def test_update_non_existent_booking(client):
    dto = BookingUpdateDTO(
        check_in=datetime(2026, 1, 1),
        check_out=datetime(2026, 1, 12),
    )

    data = dto.model_dump_json()
    response = client.put('/bookings/01JA5EZ0BBQRGDX69PNTVG3N5E', data=data)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_booking(client, db_booking):
    response = client.delete(f'/bookings/{db_booking.ulid}')
    assert response.status_code == HTTPStatus.OK


def test_delete_non_existent_booking(client):
    response = client.delete('/bookings/01JA5EZ0BBQRGDX69PNTVG3N5E')
    assert response.status_code == HTTPStatus.NOT_FOUND
