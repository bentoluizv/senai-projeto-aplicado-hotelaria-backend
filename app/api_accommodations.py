from click import echo
from flask import Blueprint, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError

bp = Blueprint("api_accommodation", __name__, url_prefix="/api/acomodacoes")


@bp.get("")
def get_accommodations():
    db = get_db()
    dao = AccommodationDAO(db)
    respository = AccommodationtRepository(dao)

    try:
        accommodations = [
            accommodation.to_dict() for accommodation in respository.find_many()
        ]
        return make_response(jsonify(accommodations), 200)

    except ValidationError as err:
        echo(err)
        return make_response({"message": err.title}, 500)


@bp.post("/cadastro")
def create_accommodation():
    accommodation_json = request.get_json()

    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)

    try:
        accommodation = Accommodation.from_dict(accommodation_json)
        repository.insert(accommodation)
        return make_response("CREATED", 201)

    except ValidationError as err:
        echo(err)
        return make_response(jsonify({"message": err.title}), 400)

    except AlreadyExistsError as err:
        echo(err)
        return make_response(jsonify({"message": err.message}), err.status)


@bp.get("/<id>")
def get_accommodation(id):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(id)

    try:
        accommodation = repository.findBy("id", str(url_param))
        return make_response(accommodation.to_json(), 200)

    except NotFoundError as err:
        echo(err)
        return make_response({"message": err.message}, err.status)


@bp.delete("/<uuid>")
def delete_accommodation(uuid):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(uuid)

    try:
        repository.delete(str(url_param))
        return make_response("DELETED", 200)

    except NotFoundError as err:
        echo(err)
        return make_response({"message": err.message}, err.status)


@bp.put("")
def update_accommodation():
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    data = request.get_json()
    echo(data)

    try:
        accommodation = Accommodation.from_dict(data)
        repository.update(accommodation)
        return "UPDATED", 201

    except ValidationError as err:
        echo(err)
        return make_response(jsonify({"message": err.title}), 400)

    except NotFoundError as err:
        echo(err)
        return make_response({"message": err.message}, err.status)
