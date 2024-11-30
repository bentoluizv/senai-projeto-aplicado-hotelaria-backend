from datetime import datetime
from http import HTTPStatus

import pytest
from click import echo

from app.entities.Booking import BookingCreateDTO, BookingUpdateDTO


def test_list_all_bookings(client):
    TOTAL_BOOKINGS = 5
    response = client.get('/bookings/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'bookings' in response.json()
    assert len(response.json()['bookings']) == TOTAL_BOOKINGS


@pytest.mark.parametrize(
    ('check_in', 'check_out', 'expected_status'),
    [
        ('2023-05-01', '2023-05-10', 1),
        ('2023-06-15', '2023-06-20', 1),
        ('2023-05-05', '2023-05-15', 1),
        ('2023-06-10', '2023-06-18', 1),
        ('2023-05-01', '2023-07-01', 3),
        ('2023-06-01', '2024-01-15', 3),
        ('2023-04-01', '2023-04-30', 0),
        ('2024-07-15', '2024-11-30', 0),
        ('2025-01-01', '2025-01-31', 0),
        ('2022-01-01', '2025-01-01', 5),
    ],
)
def test_list_all_bookings_by_period(
    client, check_in, check_out, expected_status
):
    response = client.get(
        f'/bookings/?check_in={check_in}&check_out={check_out}&page=1&per_page=50'
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'bookings' in response.json()
    echo(response.json())
    assert len(response.json()['bookings']) == expected_status


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
        == 'Página 8 fora do range. Máximo de 1 páginas.'
    )


def test_find_booking_by_id(client):
    response = client.get('/bookings/01JB3HNXD570W7V12DSQWS2XMJ')
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
        == "Booking com o ID '01JA5EZ0BBQRGDX69PNTVG3N5E' não encontrada!"
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
def test_create_new_booking(client, check_in, check_out, expected_status):
    dto = BookingCreateDTO(
        check_in=check_in,
        check_out=check_out,
        guest_document='1234325',
        accommodation_ulid='01JAFQXR26049VNR64PJE3J1W4',
    )

    data = dto.model_dump_json()
    response = client.post('/bookings', data=data)
    assert response.status_code == expected_status


def test_create_booking_with_same_period_diff_accommodation(client):
    dto1 = BookingCreateDTO(
        check_in=datetime(2024, 10, 20),
        check_out=datetime(2024, 10, 25),
        guest_document='1234325',
        accommodation_ulid='01JAFQXR26049VNR64PJE3J1W4',
    )
    dto2 = BookingCreateDTO(
        check_in=datetime(2024, 10, 20),
        check_out=datetime(2024, 10, 25),
        guest_document='8901092',
        accommodation_ulid='01JDPX3130F1SHTN6EYZKTRG6N',
    )

    data1 = dto1.model_dump_json()
    response1 = client.post('/bookings', data=data1)

    data2 = dto2.model_dump_json()
    response2 = client.post('/bookings', data=data2)

    assert response1.status_code == HTTPStatus.CREATED
    assert response2.status_code == HTTPStatus.CREATED


def test_update_booking(client):
    dto = BookingUpdateDTO(status='reservado')

    data = dto.model_dump_json()
    response = client.put('/bookings/01JB3HNXD570W7V12DSQWS2XMJ', data=data)
    assert response.status_code == HTTPStatus.OK


def test_update_booking_error(client):
    dto = BookingUpdateDTO(status='reservado')

    data = dto.model_dump_json()
    response = client.put('/bookings/01JB3HNXD570W7V12DSQWS2XMJ', data=data)
    assert response.status_code == HTTPStatus.OK

    dto = BookingUpdateDTO(status='cancelada')

    data = dto.model_dump_json()
    response = client.put('/bookings/01JB3HNXD570W7V12DSQWS2XMJ', data=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_non_existent_booking(client):
    dto = BookingUpdateDTO(status='reservado')

    data = dto.model_dump_json()
    response = client.put('/bookings/01JA5EZ0BBQRGDX69PNTVG3N5E', data=data)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_booking(client):
    response = client.delete('/bookings/01JB3HNXD570W7V12DSQWS2XMJ')
    assert response.status_code == HTTPStatus.OK


def test_delete_non_existent_booking(client):
    response = client.delete('/bookings/01JA5EZ0BBQRGDX69PNTVG3N5E')
    assert response.status_code == HTTPStatus.NOT_FOUND
