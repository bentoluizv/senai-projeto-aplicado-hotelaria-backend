from datetime import datetime
from flask import abort, redirect
from flask import Blueprint, jsonify, request
from markupsafe import escape

from app.data.dao.guest_dao import GuestDAO
from app.data.database.db import get_db

bp = Blueprint('guests', __name__, url_prefix='/hospedes')

@bp.get('/')
def hospedes():
    db = get_db()
    guest_dao = GuestDAO(db)
    guests = guest_dao.select_many()
    return jsonify(guests)


@bp.post('/cadastro')
def cria_hospede():

    if request.form is None:
        abort(400)

    guest = {
        'document': request.form['document'],
        'created_at': datetime.now().isoformat(),
        'name': request.form['name'],
        'surname': request.form['surname'],
        'country': request.form['country'],
        'phone': request.form['phone']
    }

    db = get_db()
    guest_dao = GuestDAO(db)
    guest_dao.insert(guest)

    return redirect('/hospedes')


@bp.get('/<document>')
def hospede(document):
    db = get_db()
    guest_dao = GuestDAO(db)
    url_param = escape(document)
    guest = guest_dao.select({ 'document', url_param })

    if guest is None:
        abort(404)

    return jsonify(guest)


@bp.delete('/<document>')
# deve deletar um hospede
def deletar_hospede(document):
    db = get_db()
    guest_dao = GuestDAO(db)
    url_param = escape(document)

    try:
        guest_dao.delete(url_param)
    except:
        abort(400)

    return redirect('/hospedes')


@bp.put('/<document>')
def atualizar_hospede():
# deve atualizar hospede
    guest = {
        'document': request.form['document'],
        'name': request.form['name'],
        'surname': request.form['surname'],
        'country': request.form['country'],
        'phone': request.form['phone']
    }

    db = get_db()
    guest_dao = GuestDAO(db)

    try:
        guest_dao.update(guest)
    except:
        abort(400)

    return redirect('/hospedes')