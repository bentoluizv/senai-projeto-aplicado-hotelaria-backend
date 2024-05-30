import click
from flask import Blueprint, abort, jsonify, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation


bp = Blueprint('apiacomodacoes', __name__, url_prefix='/api/acomodacoes')


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
    if request.form is None:
        abort(400)

    accommodation_dto = {
        'name': request.form['name'],
        'status': request.form['status'],
        'total_guests': request.form['total_guests'],
        'single_beds': request.form['single_beds'],
        'double_beds': request.form['double_beds'],
        'min_nights': request.form['min_nights'],
        'price': request.form['price']
    }

    accommodation =  Accommodation.from_dict(accommodation_dto)

    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)

    try:
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
        accommodation = repository.find(str(url_param))
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