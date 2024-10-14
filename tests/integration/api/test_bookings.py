from http import HTTPStatus

import pytest


def test_list_all_bookings(client):
    TOTAL_BOOKINGS = 10
    response = client.get('/bookings/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'bookings' in response.json()
    assert len(response.json()['bookings']) == TOTAL_BOOKINGS


def test_list_all_bookings_20_per_page(client):
    TOTAL_BOOKINGS = 20
    response = client.get('/bookings/?page=1&per_page=20')
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
        == 'Page 8 is out of range. There are only 6 pages.'
    )


@pytest.mark.usefixtures('_db_booking')
def test_find_booking_by_id(client):
    response = client.get('/bookings/01JA5EZ0BBQRGDX69PNTVG3N5E')
    booking = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert booking['guest']
    assert booking['accommodation']
    assert booking['budget'] > 0
