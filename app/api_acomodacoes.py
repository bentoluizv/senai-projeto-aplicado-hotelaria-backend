from ast import Try
import json
import click
from flask import Blueprint, abort, jsonify, redirect, request
from markupsafe import escape

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.entity.Accommodation import Accommodation, AccommodationDTO


bp = Blueprint('apiacomodacoes', __name__, url_prefix='/api/acomodacoes')


@bp.get('')
def acomodacoes_api():
    db = get_db()
    dao = AccommodationDAO(db)
    respository = AccommodationtRepository(dao)
    accommodation = [ accommodation.to_dict() for accommodation in respository.find_many() ]
    return jsonify(accommodation)


@bp.post('/cadastro')
def cria_acomodacoes():
    if request.form is None:
        abort(400)

    accommodationDTO_dto: AccommodationDTO = {
        'uuid': request.form['uuid'],        
        'name': request.form['name'],
        'status': request.form['status'],
        'total_guests': request.form['total_guests'],
        'single_beds': request.form['single_beds'],
        'double_beds': request.form['double_beds'],
        'min_nights': request.form['min_nights'],
        'price': request.form['price'],
        'created_at': None
    }

    

    accommodation =  Accommodation.from_dict(accommodationDTO_dto)

    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)

    try:
        repository.insert(accommodation)
        return 'CREATED', 201

    except ValueError as e:
        click.echo(e)
        abort(400)


@bp.get('/<document>')
def hospede(document):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(document)

    try:
        guest = repository.find(str(url_param))
        return jsonify(guest.to_dict())

    except ValueError:
        abort(404)


@bp.delete('/<document>')
def deletar_hospede(document):
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    url_param = escape(document)

    try:
        repository.delete(str(url_param))
        return 'DELETED', 200

    except ValueError:
        abort(404)

@bp.put('')
def atualizar_hospede():
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    raw  = request.get_json()
    guest = Accommodation.from_dict(raw)

    try:
        repository.update(guest)
        return "UPDATED", 201

    except ValueError:
        abort(404)