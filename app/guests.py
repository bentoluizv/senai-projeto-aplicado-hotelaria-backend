from datetime import datetime
from flask import abort, make_response, redirect
from flask import Blueprint, jsonify, request
from markupsafe import escape

from app.data.dao.guest_dao import GuestDAO
from app.data.database.db import get_db
from app.domain.Guests import Guest

bp = Blueprint('guests', __name__, url_prefix='/hospedes')

@bp.get('/')
def hospedes():
    db = get_db()
    guest_dao = GuestDAO(db)
    guests = guest_dao.select_many()
    return jsonify(guests) # Retorna um JSON com os dados, deve retornar um render_page com a pagina que lista todos os registros.


@bp.post('/cadastro')
def cria_hospede():
    if request.form is None:
        abort(400)
    guest =  Guest(request.form['document'], request.form['name'], request.form['surname'], request.form['country'],request.form['phone'])
    db = get_db()
    guest_dao = GuestDAO(db)
    guest_dao.insert(guest)
    return 'CREATED', 201


@bp.get('/<document>')
def hospede(document):
    db = get_db()
    guest_dao = GuestDAO(db)
    url_param = escape(document)
    guest = guest_dao.select(url_param)
    if guest is None:
        abort(404)
    return jsonify(guest.toObj())


@bp.delete('/<document>')
# deve deletar um hospede
def deletar_hospede(document):
    db = get_db()
    guest_dao = GuestDAO(db)
    url_param = escape(document)
    exists = guest_dao.select(url_param)
    if not exists:
        abort(404)
    guest_dao.delete(url_param)
    return 'DELETED', 200


@bp.put('/')
def atualizar_hospede():
# deve atualizar hospede
    db = get_db()
    guest_dao = GuestDAO(db)
    if request.form['document'] is None or request.form['document'] == '':
        abort(400)
    exists = guest_dao.select(request.form['document'])
    if not exists:
        abort(404)
    guest = Guest(request.form['document'], request.form['name'], request.form['surname'], request.form['country'],request.form['phone'], exists.created_at)
    guest_dao.update(guest)
    return 'UPDATED', 200