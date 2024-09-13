import json
from http import HTTPStatus


def test_list_all_accommodation(client):
    TOTAL_ACCOMMODATIONS = 1
    response = client.get('/accommodations')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data) == TOTAL_ACCOMMODATIONS


def test_create_accommodation(client):
    new_accommodation = json.dumps({
        'name': 'Teste Quarto',
        'status': 'Disponível',
        'total_guests': 2,
        'single_beds': 0,
        'double_beds': 1,
        'price': 1200,
        'amenities': ['wifi', 'ducha'],
    })

    response = client.post('/accommodations/', data=new_accommodation)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['content'] == 'CREATED'


def test_find_accommodation_by_id(client):
    response = client.get('/accommodations/1')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Quarto de Teste'


def test_update_accommodation(client):
    to_update = json.dumps({'status': 'Ocupado'})
    response = client.put('/accommodations/1', data=to_update)
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Quarto de Teste'
    assert data['status'] == 'Ocupado'


def test_delete_accommodation(client):
    response = client.delete('/accommodations/1')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['content'] == 'DELETED'


def test_not_found_on_delete(client):
    response = client.delete('/accommodations/7')
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data['detail'] == 'Resource with id "7" not found!'
