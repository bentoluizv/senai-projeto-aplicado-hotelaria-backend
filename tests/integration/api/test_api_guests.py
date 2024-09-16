from http import HTTPStatus

from app.schemas.Guest import GuestCreateDTO, GuestUpdateDTO


def test_create_a_guest(client):
    new_guest = GuestCreateDTO(
        document='11223445556',
        name='Teste',
        surname='Teste',
        country='Brasil',
        phone='48911111111',
    )

    response = client.post('/hospedes/', data=new_guest.model_dump_json())
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['content'] == 'CREATED'


def test_list_all_guests(client):
    response = client.get('/hospedes/')
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Bento'


def test_find_guest(client):
    response = client.get('/hospedes/b73e37e2-ddca-4bec-86a9-016b5341c36f')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Bento'


def test_update_guest(client):
    data_to_update = GuestUpdateDTO(phone='1123344556')
    response = client.put(
        '/hospedes/b73e37e2-ddca-4bec-86a9-016b5341c36f',
        data=data_to_update.model_dump_json(),
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Bento'


def test_delete_guest(client):
    response = client.delete('/hospedes/b73e37e2-ddca-4bec-86a9-016b5341c36f')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['content'] == 'DELETED'
