from ast import Try
import json
import click
from flask import Blueprint, abort, jsonify, redirect, request
from markupsafe import escape

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.data.repositories.GuestRepository import GuestRepository
from app.entity.Guests import Guest, GuestDTO


bp = Blueprint('api', __name__, url_prefix='/api/hospedes')


@bp.get('/')
def hospedes_api():
    db = get_db()
    dao = GuestDAO(db)
    respository = GuestRepository(dao)
    guests = [ guest.to_dict() for guest in respository.find_many() ]
    return jsonify(guests)


@bp.post('/cadastro/')
def cria_hospede():
    if request.form is None:
        abort(400)

    guest_dto: GuestDTO = {
        'document': request.form['document'],
        'name': request.form['name'],
        'surname': request.form['surname'],
        'country': request.form['country'],
        'phone': request.form['phone'],
        'created_at': None
    }

    guest =  Guest.from_dict(guest_dto)

    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)

    try:
        repository.insert(guest)
        return redirect('/hospedes')

    except ValueError as e:
        click.echo(e)
        abort(409)


@bp.get('/<document>/')
def hospede(document):
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    url_param = escape(document)

    try:
        guest = repository.find(str(url_param))
        return jsonify(guest.to_dict())

    except ValueError:
        abort(404)


@bp.delete('/<document>/')
def deletar_hospede(document):
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    url_param = escape(document)

    try:
        repository.delete(str(url_param))
        return 'DELETED', 200

    except ValueError:
        abort(404)

@bp.put('/')
def atualizar_hospede():
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    raw  = request.get_json()
    guest = Guest.from_dict(raw)

    try:
        repository.update(guest)
        return "UPDATED", 201

    except ValueError:
        abort(404)