import click
from flask import Blueprint, abort, jsonify, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AmenitieDAO import AmenitieDAO
from app.data.database.db import get_db

bp = Blueprint("api_amenities", __name__, url_prefix="/api/amenities")


@bp.get("")
def get_amenities():
    db = get_db()
    dao = AmenitieDAO(db)

    try:
        amenities = [amenitie for amenitie in dao.find_many()]
        return jsonify(amenities)

    except ValidationError as err:
        click.echo(err)
        abort(500)


@bp.post("/cadastro")
def create_amenitie():
    if request.form is None:
        abort(400)

    amenitie = (request.form["amenitie"],)

    db = get_db()
    dao = AmenitieDAO(db)

    try:
        dao.insert(amenitie)
        return "CREATED", 201

    except ValueError as e:
        click.echo(e)
        abort(400)


@bp.delete("/<name>")
def delete_accommodation(name):
    db = get_db()
    dao = AmenitieDAO(db)
    url_param = escape(name)

    try:
        dao.delete(str(url_param))
        return "DELETED", 200

    except ValueError:
        abort(404)
