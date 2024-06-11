import click
from flask import Blueprint, Response, abort, jsonify, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation
from app.errors.NotFoundError import NotFoundError
from app.utils.transform import transform

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
        return jsonify(accommodations)

    except ValidationError:
        abort(500)


@bp.post("/cadastro")
def create_accommodation():
    accommodation_json = request.get_json()

    if accommodation_json is None:
        abort(400)

    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)

    try:
        accommodation = Accommodation.from_dict(transform(accommodation_json))
        repository.insert(accommodation)
        return "CREATED", 201

    except ValueError as e:
        click.echo(e)
        if "Accommodation with document" in str(e):
            abort(409, "Já existe uma acomdação com este nome!")

        abort(400)


@bp.get("/<id>")
def get_accommodation(id):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(id)

    try:
        accommodation = repository.findBy("id", str(url_param))
        return accommodation.to_json()

    except NotFoundError as err:
        response = Response()
        response.status_code = err.status
        response.data = err.message
        return response


@bp.delete("/<uuid>")
def delete_accommodation(uuid):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(uuid)

    try:
        repository.delete(str(url_param))
        return "DELETED", 200

    except ValueError:
        abort(404)


@bp.put("")
def update_accommodation():
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    raw = request.get_json()
    data = {
        "uuid": raw["uuid"],
        "created_at": raw["createdAt"],
        "name": raw["name"],
        "total_guests": raw["totalGuests"],
        "single_beds": raw["singleBeds"],
        "double_beds": raw["doubleBeds"],
        "min_nights": raw["minNights"],
        "price": raw["price"],
        "amenities": raw["amenities"],
    }
    try:
        accommodation = Accommodation.from_dict(transform(data))
        repository.update(accommodation)
        return "UPDATED", 201

    except ValidationError as err:
        click.echo(err)
        abort(400)

    except ValueError as err:
        click.echo(err)
        abort(404)
