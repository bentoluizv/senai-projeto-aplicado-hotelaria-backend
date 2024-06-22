from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.schemas.AccommodationSchema import (
    AccommodationCreationalSchema,
)
from app.data.database.sqlite.db import get_db
from app.data.repository.AccommodationRepository import AccommodationRepository
from app.domain.Accommodation import Accommodation
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError

bp = Blueprint('api_accommodation', __name__, url_prefix='/acomodacoes')


@bp.get('/')
@bp.get('')
def get_all_accommodations():
    db = get_db()
    dao = AccommodationDAO(db)
    respository = AccommodationRepository(dao)
    accommodations = respository.find_many()
    serializable_accommodations = [
        accommodation.model_dump() for accommodation in accommodations
    ]

    return jsonify(serializable_accommodations), HTTPStatus.OK


@bp.get('/<id>')
@bp.get('/<id>/')
def get_accommodation_by_id(id):
    try:
        db = get_db()
        dao = AccommodationDAO(db)
        respository = AccommodationRepository(dao)
        url_param = escape(id)

        accommodation = respository.find(int(url_param))
        serializable_accommodation = accommodation.model_dump()

        return jsonify(serializable_accommodation)

    except NotFoundError as err:
        return make_response(err.json(), err.status_code)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.post('/cadastro/')
def create_accommodation():
    try:
        db = get_db()
        dao = AccommodationDAO(db)
        respository = AccommodationRepository(dao)
        data = request.get_json()

        accommodation = AccommodationCreationalSchema(**data)

        respository.create(accommodation)

        return make_response('CREATED', HTTPStatus.CREATED)

    except AlreadyExistsError as err:
        return make_response(err.json(), err.status_code)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.put('/<id>')
@bp.put('/<id>/')
def update_accommodation(id):
    try:
        db = get_db()
        dao = AccommodationDAO(db)
        repository = AccommodationRepository(dao)
        data = request.get_json()

        accommodation = Accommodation(**data)

        repository.update(accommodation)

        return make_response({}, HTTPStatus.NO_CONTENT)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)

    except NotFoundError as err:
        return make_response(err.json(), HTTPStatus.NOT_FOUND)


@bp.delete('/<id>')
@bp.delete('/<id>/')
def delete_accommodation(id):
    try:
        db = get_db()
        dao = AccommodationDAO(db)
        repository = AccommodationRepository(dao)
        url_param = escape(id)
        repository.delete(int(url_param))

        return make_response({}, HTTPStatus.NO_CONTENT)

    except NotFoundError as err:
        return make_response(err.json(), err.status_code)
