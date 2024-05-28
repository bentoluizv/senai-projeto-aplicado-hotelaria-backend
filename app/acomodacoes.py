from flask import render_template
from flask import Blueprint

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository

bp = Blueprint('accommodation', __name__, url_prefix='/acomodacoes')

@bp.get('/')
def hospedes():
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    accommodation = [ accommodation.to_dict() for accommodation in repository.find_many() ]
    return render_template('acomodacoes.html', rows=accommodation)


@bp.get('/cadastro/')
def cadastro():
    return render_template('cadastroHospedes.html')




