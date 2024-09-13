import json
from http import HTTPStatus


def test_list_all_amenties(client):
    TOTAL_AMENITIES = 2
    response = client.get('/amenities/')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data) == TOTAL_AMENITIES


def test_create_amenitie(client):
    new_amenitie = json.dumps({'name': 'piscina'})
    response = client.post('/amenities/', data=new_amenitie)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['content'] == 'CREATED'
