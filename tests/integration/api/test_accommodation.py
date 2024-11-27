from http import HTTPStatus

from app.entities.Accommodation import (
    AccommodationCreateDTO,
    AccommodationUpdateDTO,
)


def test_list_all_accommodation(client):
    TOTAL_ACCOMMODATION = 10
    response = client.get('/accommodations/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'accommodations' in response.json()
    assert len(response.json()['accommodations']) == TOTAL_ACCOMMODATION


def test_list_all_accommodations_2_per_page(client):
    TOTAL_ACCOMMODATIONS = 2
    response = client.get('/accommodations/?page=1&per_page=2')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'accommodations' in response.json()
    assert len(response.json()['accommodations']) == TOTAL_ACCOMMODATIONS


def test_list_all_out_range(client):
    response = client.get('/accommodations/?page=8&per_page=5')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert isinstance(response.json(), dict)
    assert 'detail' in response.json()
    assert (
        response.json()['detail']
        == 'Page 8 is out of range. There are only 3 pages.'
    )


def test_find_accommodation_by_id(client):
    response = client.get('/accommodations/01JAFQXR26049VNR64PJE3J1W4')
    accommodation = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert accommodation['name'] == 'Beachfront Villa'


def test_not_found_accommodation_by_id(client):
    response = client.get('/accommodations/01JA5EZ0BBQRGDX69PNTVG3N5E')
    accommodation = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json(), dict)
    assert (
        accommodation['detail']
        == """Accommodation with ID '01JA5EZ0BBQRGDX69PNTVG3N5E' not found."""
    )


def test_create_new_accommodations(
    client,
):
    dto = AccommodationCreateDTO(
        name='Teste Acomodação',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=120,
        amenities=[],
    )

    data = dto.model_dump_json()
    response = client.post('/accommodations', data=data)
    assert response.status_code == HTTPStatus.CREATED


def test_create_2_new_accommodations_in_a_row(
    client,
):
    dto = AccommodationCreateDTO(
        name='Teste Acomodação',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=120,
        amenities=[],
    )

    dto2 = AccommodationCreateDTO(
        name='Teste Acomodação 2',
        total_guests=1,
        single_beds=1,
        double_beds=0,
        price=120,
        amenities=[],
    )

    data = dto.model_dump_json()
    data2 = dto2.model_dump_json()
    response = client.post('/accommodations', data=data)
    response2 = client.post('/accommodations', data=data2)

    assert response.status_code == HTTPStatus.CREATED
    assert response2.status_code == HTTPStatus.CREATED


def test_update_accommodation(client):
    dto = AccommodationUpdateDTO(name='Super Teste')

    data = dto.model_dump_json()
    response = client.put(
        '/accommodations/01JAFQXR26049VNR64PJE3J1W4', data=data
    )
    assert response.status_code == HTTPStatus.OK


def test_update_non_existent_accommodation(client):
    dto = AccommodationUpdateDTO(name='Super Teste')

    data = dto.model_dump_json()
    response = client.put(
        '/accommodations/01JA5EZ0BBQRGDX69PNTVG3N5E', data=data
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_accommodation(client, db_accommodation):
    response = client.delete(f'/accommodations/{db_accommodation.ulid}')
    assert response.status_code == HTTPStatus.OK


def test_delete_non_existent_accommodation(client):
    response = client.delete('/accommodation/01JA5EZ0BBQRGDX69PNTVG3N5E')
    assert response.status_code == HTTPStatus.NOT_FOUND
