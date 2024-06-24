import json
from http import HTTPStatus


def test_api_should_get_all_bookings(client):
    response = client.get('/reservas/')
    assert response.status_code == HTTPStatus.OK


def test_api_should_get_an_especific_booking_by_uuid(client):
    response = client.get('/reservas/e08f76e8-0e71-4a48-a85a-bf7e8f61479e')
    assert response.status_code == HTTPStatus.OK


def test_api_should_return_404_if_not_found(client):
    response = client.get(
        '/api/reservas/e08f76e8-0e71-4a48-a85a-bf7e8s71479e/'
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_should_create_a_booking(client):
    data = {
        'locator': 'AS341243',
        'status': 'Finalizada',
        'check_in': '2024-02-27T10:30:00.156342',
        'check_out': '2024-03-03T10:30:00.156342',
        'guest_document': '00157624242',
        'accommodation_id': 1,
        'budget': 1200,
    }

    response = client.post(
        '/reservas/cadastro/',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.text == 'CREATED'


def test_api_should_return_422_on_bad_request_from_client(client):
    response = client.post(
        '/reservas/cadastro/',
        data=json.dumps({}),
        headers={'content-type': 'application/json'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_api_should_update_a_booking(client):
    data = {
        'uuid': 'e08f76e8-0e71-4a48-a85a-bf7e8f61479e',
        'locator': 'AB897564',
        'status': 'Finalizada',
        'created_at': '2024-06-18T17:30:00',
        'check_in': '2024-06-06T08:30:00',
        'check_out': '2024-06-18T10:30:00.156342',
        'guest_document': '00157624242',
        'accommodation_id': 6,
        'budget': 1200,
    }

    response = client.put(
        '/reservas/e08f76e8-0e71-4a48-a85a-bf7e8f61479e',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_should_return_404_on_updating_non_existing_booking(client):
    data = {
        'uuid': 'e08f76e8-0e71-3k49-a85a-bf7e8f61479e',
        'locator': 'AB897564',
        'status': 'Finalizada',
        'created_at': '2024-06-18T17:30:00',
        'check_in': '2024-06-06T08:30:00',
        'check_out': '2024-06-18T10:30:00.156342',
        'guest_document': '00157624242',
        'accommodation_id': 6,
        'budget': 1200,
    }
    response = client.put(
        '/reservas/48732618050',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_should_delete_a_booking(client):
    response = client.delete('/reservas/e08f76e8-0e71-4a48-a85a-bf7e8f61479e/')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_should_return_404_when_deleting_non_existing_booking(client):
    response = client.delete('/reservas/e08f76e8-0e71-3k49-a85a-bf7e8f61479e/')
    assert response.status_code == HTTPStatus.NOT_FOUND
