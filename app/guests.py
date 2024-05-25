from flask import render_template
from flask import Blueprint

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.data.repositories.GuestRepository import GuestRepository

bp = Blueprint('guests', __name__, url_prefix='/hospedes')

@bp.get('/')
def hospedes():
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    guests = [ guest.to_dict() for guest in repository.find_many() ]
    return render_template('hospedes.html', rows=guests)


@bp.get('/cadastro/')
def cadastro():
    return render_template('cadastroHospedes.html')


@bp.get('/<document>/')
def editar(document):
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    guest = repository.find(document)
    return render_template('alteraHospedes.html', guest=guest.to_dict())