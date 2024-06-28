from datetime import datetime
from http import HTTPStatus


def test_create_booking(client):
    data = {
        'locator': 'KS928374',
        'status': 'Confirmado',
        'check_in': datetime(2024, 12, 8).isoformat(),
        'check_out': datetime(2024, 12, 12).isoformat(),
        'budget': 8200,
        'guest_document': '45678912300',
        'accommodation_id': 1,
    }

    response = client.post('/reservas', json=data)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert 'created_at' in data
    assert 'uuid' in data


def test_list_all_bookings(client):
    TOTAL_ACCOMMODATIONS = 2
    response = client.get('/reservas')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data['bookings']) == TOTAL_ACCOMMODATIONS


def test_find_booking(client):
    response = client.get('/reservas/b2a72d82-71e1-11e9-8f9e-2a86e4085a59')
    data = response.json()
    assert response.status_code == HTTPStatus.OK

    assert data['accommodation']['name'] == 'Charrua (Bus)'
    assert data['guest']['name'] == 'Maria'


def test_update_booking(client):
    data = {
        'locator': 'KS928374',
        'status': 'Aguardando Pagamento',
        'check_in': datetime(2024, 12, 8).isoformat(),
        'check_out': datetime(2024, 12, 22).isoformat(),
        'budget': 12999,
        'guest_document': '45678912300',
        'accommodation_id': 1,
    }

    response = client.put(
        '/reservas/b2a72d82-71e1-11e9-8f9e-2a86e4085a59', json=data
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_guest(client):
    response = client.delete('/reservas/b2a72d82-71e1-11e9-8f9e-2a86e4085a59')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_not_found_on_delete_booking(client):
    response = client.delete('/reservas/b2a72d82-71e1-11e9-6d5v-2a86e4085a59')
    assert response.status_code == HTTPStatus.NOT_FOUND
