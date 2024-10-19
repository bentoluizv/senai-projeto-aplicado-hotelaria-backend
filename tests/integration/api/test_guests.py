from http import HTTPStatus

from app.entities.Guest import GuestCreateDTO, GuestUpdateDTO


def test_list_all_guests(client):
    TOTAL_GUESTS = 10
    response = client.get('/guests/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'guests' in response.json()
    assert len(response.json()['guests']) == TOTAL_GUESTS


def test_list_all_guests_2_per_page(client):
    TOTAL_GUESTS = 2
    response = client.get('/guests/?page=1&per_page=2')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'guests' in response.json()
    assert len(response.json()['guests']) == TOTAL_GUESTS


def test_list_all_out_range(client):
    response = client.get('/guests/?page=8&per_page=5')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert isinstance(response.json(), dict)
    assert 'detail' in response.json()
    assert (
        response.json()['detail']
        == 'Page 8 is out of range. There are only 2 pages.'
    )


def test_find_guest_by_id(client, db_guest):
    response = client.get(f'/guests/{db_guest.ulid}')
    guest = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert guest['document'] == '2672713987'


def test_not_found_guest_by_id(client):
    response = client.get('/guests/01JA5EZ0BBQRGDX69PNTVG3N5E')
    guest = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json(), dict)
    assert (
        guest['detail']
        == """Guest with ID '01JA5EZ0BBQRGDX69PNTVG3N5E' not found."""
    )


def test_create_new_guest(
    client,
):
    dto = GuestCreateDTO(
        document='122434556',
        name='Teste Guest',
        surname='Teste Testando',
        phone='47389111111',
        country='Brasil',
    )

    data = dto.model_dump_json()
    response = client.post('/guests', data=data)
    assert response.status_code == HTTPStatus.CREATED


def test_update_guest(client, db_guest):
    dto = GuestUpdateDTO(name='Super Teste')

    data = dto.model_dump_json()
    response = client.put(f'/guests/{db_guest.ulid}', data=data)
    assert response.status_code == HTTPStatus.OK


def test_update_non_existent_guest(client):
    dto = GuestUpdateDTO(name='Super Teste')

    data = dto.model_dump_json()
    response = client.put('/guests/01JA5EZ0BBQRGDX69PNTVG3N5E', data=data)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_guest(client, db_guest):
    response = client.delete(f'/guests/{db_guest.ulid}')
    assert response.status_code == HTTPStatus.OK


def test_delete_non_existent_guest(client):
    response = client.delete('/guest/01JA5EZ0BBQRGDX69PNTVG3N5E')
    assert response.status_code == HTTPStatus.NOT_FOUND
