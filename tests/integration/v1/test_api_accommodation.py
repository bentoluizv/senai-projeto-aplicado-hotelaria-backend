import json
from http import HTTPStatus

from app.database.schemas.AccommodationSchema import (
    AccommodationCreationalSchema,
    AccommodationDB,
)


def test_api_should_get_all_accommodations(client):
    response = client.get('/acomodacoes/')
    assert response.status_code == HTTPStatus.OK


def test_api_should_get_an_especific_accommodation_by_id(client):
    response = client.get('/acomodacoes/1')
    assert response.status_code == HTTPStatus.OK


def test_api_should_return_404_if_not_found(client):
    response = client.get('/api/acomodacoes/12/')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_should_create_a_accommodation(client):
    data = AccommodationCreationalSchema(**{
        'name': 'Churrasqueira',
        'status': 'Disponivel',
        'total_guests': 6,
        'single_beds': 0,
        'double_beds': 2,
        'price': 350,
        'amenities': ['wifi', 'ducha'],
    })

    response = client.post(
        '/acomodacoes/cadastro/',
        data=json.dumps(data.model_dump()),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.text == 'CREATED'


def test_api_should_return_422_on_bad_request_from_client(client):
    response = client.post(
        '/acomodacoes/cadastro/',
        data=json.dumps({}),
        headers={'content-type': 'application/json'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_api_should_delete_a_accommodation(client):
    response = client.delete('/acomodacoes/1/')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_should_return_404_when_deleting_non_existing_accommodation(
    client,
):
    response = client.delete('/acomodacoes/12/')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_should_update_a_accommodation(client):
    data = AccommodationDB(**{
        'id': 1,
        'name': 'Churrasqueira',
        'status': 'Disponivel',
        'total_guests': 6,
        'single_beds': 0,
        'double_beds': 2,
        'price': 350,
        'amenities': ['wifi', 'ducha'],
    })

    response = client.put(
        '/acomodacoes/1/',
        data=json.dumps(data.model_dump()),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_should_return_404_on_updating_non_existing_accommodation(client):
    data = AccommodationDB(**{
        'id': 32,
        'name': 'Churrasqueira',
        'status': 'Disponivel',
        'total_guests': 6,
        'single_beds': 0,
        'double_beds': 2,
        'price': 350,
        'amenities': ['wifi', 'ducha'],
    })
    response = client.put(
        '/acomodacoes/32',
        data=json.dumps(data.model_dump()),
        headers={'content-type': 'application/json'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
