import click
from flask import Blueprint, abort, jsonify, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation


bp = Blueprint('api_accommodation', __name__, url_prefix='/api/acomodacoes')


@bp.get('')
def get_accommodations():
    db = get_db()
    dao = AccommodationDAO(db)
    respository = AccommodationtRepository(dao)

    try:
        accommodations = [ accommodation.to_dict() for accommodation in respository.find_many() ]
        return jsonify(accommodations)

    except ValidationError as err:
        click.echo(err)
        abort(500)


@bp.post('/cadastro')
def create_accommodation():
    accommodation_json = request.get_json()

    if accommodation_json is None:
        abort(400)
    click.echo(accommodation_json)

    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)

    try:
        accommodation =  Accommodation.from_dict(accommodation_json)
        repository.insert(accommodation)
        return 'CREATED', 201

    except ValueError as e:
        click.echo(e)
        abort(400)


@bp.get('/<uuid>')
def get_accommodation(uuid):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(uuid)

    try:
        accommodation = repository.findBy("uuid",  str(url_param))
        return accommodation.to_json()

    except ValueError:
        abort(404)


@bp.delete('/<uuid>')
def delete_accommodation(uuid):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(uuid)

    try:
        repository.delete(str(url_param))
        return 'DELETED', 200

    except ValueError:
        abort(404)

@bp.put('')
def update_accommodation():
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    raw  = request.get_json()

    try:
        accommodation = Accommodation.from_dict(raw)
        repository.update(accommodation)
        return "UPDATED", 201

    except ValidationError as err:
        click.echo(err)
        abort(400)

    except ValueError as err:
        click.echo(err)
        abort(404)