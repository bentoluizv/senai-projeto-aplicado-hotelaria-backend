from http import HTTPStatus


def test_create_accommodation(client):
    data = {
        'name': 'Churrasqueira',
        'status': 'Disponivel',
        'total_guests': 6,
        'single_beds': 0,
        'double_beds': 2,
        'min_nights': 2,
        'price': 350,
        'amenities': ['wifi', 'toalhas'],
    }

    response = client.post('/acomodacoes', json=data)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert 'created_at' in data


def test_list_all_accommodation(client):
    TOTAL_ACCOMMODATIONS = 6
    response = client.get('/acomodacoes')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data['accommodations']) == TOTAL_ACCOMMODATIONS


def test_find_accommodation(client):
    response = client.get('/acomodacoes/6')
    data = response.json()
    assert response.status_code == HTTPStatus.OK

    assert data['name'] == 'Estacionamento para overlanders'


def test_update_accommodation(client):
    data = {
        'id': 1,
        'name': 'Domo',
        'status': 'Ocupado',
        'total_guests': 4,
        'single_beds': 2,
        'double_beds': 2,
        'min_nights': 2,
        'price': 1380,
        'amenities': ['wifi', 'toalhas'],
    }
    response = client.put('/acomodacoes/1', json=data)

    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['status'] == 'Ocupado'
    assert data['amenities'] == [
        {'id': 2, 'name': 'wifi'},
        {'id': 7, 'name': 'toalhas'},
    ]


def test_delete_guest(client):
    response = client.delete('/acomodacoes/1')
    assert response.status_code == HTTPStatus.NO_CONTENT
