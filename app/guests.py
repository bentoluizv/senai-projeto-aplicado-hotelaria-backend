from datetime import datetime
from flask import abort, make_response, redirect, render_template
from flask import Blueprint, jsonify, request
from markupsafe import escape

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.data.repositories.GuestRepository import GuestRepository
from app.entity.Guests import Guest, GuestDTO

bp = Blueprint('guests', __name__, url_prefix='/hospedes')

@bp.get('/')
def hospedes():
    db = get_db()
    dao = GuestDAO(db)
    respository = GuestRepository(dao)
    guests = [ guest.to_dict() for guest in respository.find_many() ]
    return jsonify(guests)


@bp.post('/cadastro')
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
    repository.insert(guest)

    return 'CREATED', 201


@bp.get('/<document>')
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




@bp.delete('/<document>')
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

    if request.form['document'] is None or request.form['document'] == '':
        abort(400)

    guest_dto: GuestDTO = {
        'document': request.form['document'],
        'name': request.form['name'],
        'surname': request.form['surname'],
        'country': request.form['country'],
        'phone': request.form['phone'],
        'created_at': None
    }
    try:
        guest = Guest.from_dict(guest_dto)
        repository.update(guest)
        return 'UPDATED', 200

    except:
        abort(404)

@bp.get('/list')
def list():

    # Connect to the SQLite3 datatabase and
    # SELECT  Rows from the guest table.
    db = get_db()
    guest_dao = GuestDAO(db)
    rows = guest_dao.find_many()


    # Send the results of the SELECT to the list.html page
    return render_template("list.html", rows=rows)