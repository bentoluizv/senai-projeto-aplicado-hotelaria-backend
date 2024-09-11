import json
from http import HTTPStatus


def test_api_post(client):
    data = json.dumps({
        'email': 'teste@gmail.com',
        'password': 'supersecretpassword',
        'password2': 'supersecretpassword',
        'role': 'admin',
    })
    response = client.post('/users', data=data)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['content'] == 'CREATED'


def test_api_post_already_exist_error(client):
    data = json.dumps({
        'email': 'teste@gmail.com',
        'password': 'supersecretpassword',
        'password2': 'supersecretpassword',
        'role': 'admin',
    })
    client.post('/users', data=data)
    response = client.post('/users', data=data)
    data = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        data['detail'] == 'Resource with id "teste@gmail.com" already exists!'
    )
