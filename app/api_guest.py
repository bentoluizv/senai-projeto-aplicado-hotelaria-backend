import click
from flask import Blueprint, abort, jsonify, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.data.repositories.GuestRepository import GuestRepository
from app.entity.Guests import Guest
from app.utils.transform import transform
bp = Blueprint("api_guest", __name__, url_prefix="/api/hospedes")


@bp.get("")
def get_guests():
    db = get_db()
    dao = GuestDAO(db)
    respository = GuestRepository(dao)

    try:
        guests = [guest.to_dict() for guest in respository.find_many()]
        return jsonify(guests)

    except ValidationError as err:
        click.echo(err)
        abort(500)


@bp.post("/cadastro")
def create_guest():
    guests = request.get_json()
    if guests is None or guests == {}:
        abort(400)
    try:
        guest = Guest.from_dict(guests)

    except ValidationError as err:
        click.echo(err)
        if "The CPF used as a document is invalid" in str(err):
            abort(409, "Digite um CPF válido!")
        abort(400)

    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)

    try:
        repository.insert(guest)
        return "CREATED", 201

    except ValueError as err:
        click.echo(err)
        abort(409, str(err))


@bp.get("/<document>")
def get_guest(document):
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    url_param = escape(document)

    try:
        guest = repository.findBy("document", str(url_param))
        return guest.to_json()

    except ValueError as err:
        click.echo(err)
        abort(404)


@bp.delete("/<document>")
def delete_guest(document):
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    url_param = escape(document)

    try:
        repository.delete(str(url_param))
        return "DELETED", 200

    except ValueError as err:
        click.echo(err)
        abort(404)


@bp.put("")
def update_guest():
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    raw = request.get_json()
    data = {   
        'document': raw['document'],
        'name': raw['name'],
        'surname': raw['surname'],
        'phone': raw['phone'],
        'country': raw['country'],
        'created_at': raw['created_at']
    }

    try:
        guest = Guest.from_dict(transform(data))
        repository.update(guest)
        return "UPDATED", 201

    except ValidationError as err:
        click.echo(err)
        abort(400)

    except ValueError as err:
        click.echo(err)
        abort(404)
