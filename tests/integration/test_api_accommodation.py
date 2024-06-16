import json


def test_api_should_get_all_accommodations(client):
    response = client.get("/api/acomodacoes/")
    accommodations = json.loads(response.data)

    assert len(accommodations) == 6
    assert response.status_code == 200


def test_api_should_get_an_accommodation_by_id(client):
    response = client.get("/api/acomodacoes/1/")
    accommodation = json.loads(response.data)

    assert accommodation["name"] == "Domo"
    assert response.status_code == 200


def test_api_should_return_status_code_404(client):
    response = client.get("/api/acomodacoes/12/")
    assert response.status_code == 404


def test_api_should_create_an_accommodation(client):
    accommodation_dto = {
        "id": None,
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "amenities": ["wifi"],
    }

    response = client.post(
        "/api/acomodacoes/cadastro/",
        data=json.dumps(accommodation_dto),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 201
    assert response.text == "CREATED"


def test_api_should_return_status_code_400(client):
    response = client.post(
        "/api/hospedes/cadastro/",
        data=json.dumps({}),
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 400


def test_api_should_delete_an_accommodation(client):
    response = client.delete("/api/acomodacoes/1/")
    assert response.status_code == 200
    assert response.text == "DELETED"


def test_api_should_return_status_code_404_on_delete(client):
    response = client.delete("/api/acomodacoes/8/")
    assert response.status_code == 404


def test_api_should_update_an_accommodation(client):
    data = {
        "id": 1,
        "created_at": "2024-06-07T13:43:24.494889",
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "amenities": ["wifi"],
    }

    response = client.put(
        "/api/acomodacoes/",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 201
    assert response.text == "UPDATED"


def test_api_should_return_status_code_404_on_update(client):
    data = {
        "id": 12,
        "created_at": "",
        "name": "Quarto Individual",
        "status": "Disponível",
        "total_guests": 1,
        "single_beds": 1,
        "double_beds": 0,
        "min_nights": 2,
        "price": 180,
        "amenities": ["wifi"],
    }
    response = client.put(
        "/api/acomodacoes/",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 404
