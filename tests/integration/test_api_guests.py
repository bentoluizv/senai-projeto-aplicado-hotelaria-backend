from http import HTTPStatus

import pytest


@pytest.mark.skip()
def test_create_a_guest(client):
    data = {
        'document': '00157624242',
        'name': 'Bento Luiz',
        'surname': 'Machado',
        'country': 'Brasil',
        'phone': '48992054211',
    }
    response = client.post('/hospedes', json=data)
    data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert 'created_at' in data


@pytest.mark.skip()
def test_list_all_guests(client):
    TOTAL_GUESTS = 5
    response = client.get('/hospedes')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data['guests']) == TOTAL_GUESTS


@pytest.mark.skip()
def test_find_guest(client):
    response = client.get('/hospedes/98765432100')
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Maria'


@pytest.mark.skip()
def test_update_guest(client):
    data = {
        'document': '98765432100',
        'name': 'Maria de Lurdes',
        'surname': 'Machado',
        'country': 'Brasil',
        'phone': '489998765467',
    }
    response = client.put('/hospedes/98765432100', json=data)

    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Maria de Lurdes'


@pytest.mark.skip()
def test_delete_guest(client):
    response = client.delete('/hospedes/98765432100')
    assert response.status_code == HTTPStatus.NO_CONTENT
