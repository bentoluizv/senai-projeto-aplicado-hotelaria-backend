import json
from http import HTTPStatus


def test_find_user_by_id(client, db_user):
    response = client.get(f'/users/{db_user.ulid}')
    user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert user['ulid'] == '01JAKF4V6FMQ7BEB62XVCA9KZH'


def test_not_found_user_by_id(client):
    response = client.get('/users/01JAKF4V6FMQ7BEB62XVCA9KZH')
    user = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json(), dict)
    assert (
        user['detail']
        == """User with ID '01JAKF4V6FMQ7BEB62XVCA9KZH' not found."""
    )


def test_create_new_users(
    client,
):
    # TODO: No teste ao usar a classe pydantic UserCreateDTO
    # temos um erro de validão pois a API vai chamar ela
    # novamente e na segunda chamada o valor de password
    # está diferente de password 2 causando um erro de validação

    dto = {
        'email': 'bentoluizv@gmail.com',
        'password': '12334',
        'password2': '12334',
        'role': 'admin',
    }

    data = json.dumps(dto)
    response = client.post('/users/', data=data)
    assert response.status_code == HTTPStatus.CREATED
