import json
from http import HTTPStatus


def test_api_should_get_all_guests(client):
    response = client.get('/hospedes/')
    assert response.status_code == HTTPStatus.OK


def test_api_should_get_an_especific_guest_by_document(client):
    response = client.get('/hospedes/00157624242')
    assert response.status_code == HTTPStatus.OK


def test_api_should_return_404_if_not_found(client):
    response = client.get('/api/hospedes/00157624/')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_should_create_a_guest(client):
    data = {
        'document': '03093331056',
        'name': 'Ana',
        'surname': 'Costa',
        'country': 'Brazil',
        'phone': '48xxxxxxxxxx',
    }

    response = client.post(
        '/hospedes/cadastro/',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.text == 'CREATED'


def test_api_should_return_400_on_bad_request_from_client(client):
    response = client.post(
        '/hospedes/cadastro/',
        data=json.dumps({}),
        headers={'content-type': 'application/json'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_api_should_delete_a_guest(client):
    response = client.delete('/hospedes/00157624242/')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_should_return_404_when_deleting_non_existing_guest(client):
    response = client.delete('/hospedes/0015242/')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_should_update_a_guest(client):
    data = {
        'document': '00157624242',
        'created_at': '2024-06-22T08:39:24.635735',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '48992054211',
    }

    response = client.put(
        '/hospedes/00157624242',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_should_return_404_on_updating_non_existing_guest(client):
    data = {
        'document': '48732618050',
        'created_at': '2024-06-22T08:39:24.635735',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '48992054211',
    }
    response = client.put(
        '/hospedes/48732618050',
        data=json.dumps(data),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
