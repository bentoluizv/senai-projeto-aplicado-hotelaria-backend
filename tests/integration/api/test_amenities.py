from http import HTTPStatus

from app.entities.Amenitie import AmenitieCreateDTO


def test_list_all_amenities(client):
    TOTAL_AMENITIES = 6
    response = client.get('/amenities/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'amenities' in response.json()
    assert len(response.json()['amenities']) == TOTAL_AMENITIES


def test_list_all_amenities_2_per_page(client):
    TOTAL_AMENITIES = 2
    response = client.get('/amenities/?page=1&per_page=2')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'amenities' in response.json()
    assert len(response.json()['amenities']) == TOTAL_AMENITIES


def test_list_all_out_range(client):
    response = client.get('/amenities/?page=8&per_page=5')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert isinstance(response.json(), dict)
    assert 'detail' in response.json()
    assert (
        response.json()['detail']
        == 'Página 8 fora do range. Máximo de 2 páginas.'
    )


def test_find_amenitie_by_id(client):
    response = client.get('/amenities/1')
    amenitie = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert amenitie['name'] == 'WiFi'


def test_not_found_amenitie_by_id(client):
    response = client.get('/amenities/84')
    guest = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json(), dict)
    assert guest['detail'] == """Amenitie com o ID '84' não encontrada!"""


def test_create_new_amenitie(
    client,
):
    dto = AmenitieCreateDTO(
        name='Teste Amenitie',
    )

    data = dto.model_dump_json()
    response = client.post('/amenities', data=data)
    assert response.status_code == HTTPStatus.CREATED
