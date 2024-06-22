from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.sqlite.db import get_db
from app.data.repository.GuestRepository import GuestRepository
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError

bp = Blueprint('api_guest', __name__, url_prefix='/hospedes')


@bp.get('/')
@bp.get('')
def get_all_guests():
    db = get_db()
    dao = GuestDAO(db)
    repository = GuestRepository(dao)
    guests = repository.find_many()
    serializable_guests = [guest.model_dump() for guest in guests]

    return jsonify(serializable_guests)


@bp.get('/<document>')
@bp.get('/<document>/')
def get_guest_by_id(document):
    try:
        db = get_db()
        dao = GuestDAO(db)
        respository = GuestRepository(dao)
        url_param = escape(document)
        guest = respository.find(str(url_param))

        return jsonify(guest.model_dump())

    except NotFoundError as err:
        return make_response(err.json(), err.status_code)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.post('/cadastro')
@bp.post('/cadastro/')
def create_guest():
    try:
        db = get_db()
        dao = GuestDAO(db)
        repository = GuestRepository(dao)
        data = request.get_json()
        repository.create(data)

        return make_response('CREATED', HTTPStatus.CREATED)

    except AlreadyExistsError as err:
        return make_response(err.json(), err.status_code)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.put('/<document>')
@bp.put('/<document>/')
def update_guest(document):
    try:
        db = get_db()
        dao = GuestDAO(db)
        repository = GuestRepository(dao)
        data = request.get_json()
        repository.update(data)

        return make_response({}, HTTPStatus.NO_CONTENT)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)

    except NotFoundError as err:
        return make_response(err.json(), HTTPStatus.NOT_FOUND)


@bp.delete('/<document>')
@bp.delete('/<document>/')
def delete_guest(document):
    try:
        db = get_db()
        dao = GuestDAO(db)
        repository = GuestRepository(dao)
        url_param = escape(document)
        repository.delete(document=str(url_param))

        return make_response({}, HTTPStatus.NO_CONTENT)

    except NotFoundError as err:
        return make_response(err.json(), err.status_code)


@bp.get('/<document>/reservas/')
@bp.get('/<document>/reservas')
def get_guests_with_bookings(document):
    return make_response({}, HTTPStatus.NOT_IMPLEMENTED)
