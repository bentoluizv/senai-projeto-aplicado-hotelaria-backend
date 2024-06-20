import json
from http import HTTPStatus

import pytest


@pytest.mark.skip()
def test_api_should_get_all_guests(client):
    response = client.get('/api/hospedes/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skip()
def test_api_should_get_an_especific_guest_by_document(client):
    response = client.get('/api/hospedes/00157624242/')
    guests = json.loads(response.data)
    assert guests['name'] == 'Bento'
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skip()
def test_api_should_get_all_bookings_from_an_especific_guest_by_document(
    client,
):
    response = client.get('/api/hospedes/00157624242/reservas/')
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['guest']['name'] == 'Bento'
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skip()
def test_api_should_return_404_if_not_found(client):
    response = client.get('/api/hospedes/00157624/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.skip()
def test_api_should_create_a_guest(client):
    guest_dto = {
        'document': '03093331056',
        'name': 'Ana',
        'surname': 'Costa',
        'country': 'Brazil',
        'phone': '48xxxxxxxxxx',
    }

    response = client.post(
        '/api/hospedes/cadastro/',
        data=json.dumps(guest_dto),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.text == 'CREATED'


@pytest.mark.skip()
def test_api_should_return_400_on_bad_request_from_client(client):
    response = client.post(
        '/api/hospedes/cadastro/',
        data=json.dumps({}),
        headers={'content-type': 'application/json'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.skip()
def test_api_should_delete_a_guest(client):
    response = client.delete('/api/hospedes/00157624242/')
    assert response.status_code == HTTPStatus.OK
    assert response.text == 'DELETED'


@pytest.mark.skip()
def test_api_should_return_404_when_deleting_non_existing_guest(client):
    response = client.delete('/api/hospedes/0015242/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.skip()
def test_api_should_update_a_guest(client):
    data = {
        'document': '00157624242',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '48992054211',
    }

    response = client.put(
        '/api/hospedes/',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.text == 'UPDATED'


@pytest.mark.skip()
def test_api_should_return_404_on_updating_non_existing_guest(client):
    data = {
        'document': '48732618050',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '48992054211',
    }
    response = client.put(
        '/api/hospedes/',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
