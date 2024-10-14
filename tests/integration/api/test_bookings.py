from http import HTTPStatus


def test_list_all_bookings(client):
    TOTAL_BOOKINGS = 10
    response = client.get('/bookings/?page=1&per_page=10')
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
    response = client.get('/bookings/?page=5&per_page=20')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'bookings' in response.json()
    assert len(response.json()['bookings']) == 0
