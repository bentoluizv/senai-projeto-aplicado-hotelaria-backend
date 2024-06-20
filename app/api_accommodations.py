from http import HTTPStatus

from flask import Blueprint, abort, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.sqlite.db import get_db
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.schemas.AccommodationSchema import AccommodationSchema

bp = Blueprint('api_accommodation', __name__, url_prefix='/api/acomodacoes')


@bp.get('/')
def get_accommodations():
    db = get_db()
    dao = AccommodationDAO(db)

    try:
        accommodations = [
            accommodation.model_dump() for accommodation in dao.find_many()
        ]
        return jsonify(accommodations), HTTPStatus.OK

    except ValidationError as err:
        return abort(HTTPStatus.UNPROCESSABLE_ENTITY, err.json())


@bp.post('/cadastro/')
def create_accommodation():
    accommodation_json = request.get_json()

    db = get_db()
    dao = AccommodationDAO(db)

    parsed_dto = {
        'name': accommodation_json['name'],
        'total_guests': int(accommodation_json['total_guests']),
        'single_beds': int(accommodation_json['single_beds']),
        'double_beds': int(accommodation_json['double_beds']),
        'min_nights': int(accommodation_json['min_nights']),
        'price': int(accommodation_json['price']),
        'amenities': accommodation_json['amenities'],
    }
    try:
        accommodation = AccommodationSchema(**parsed_dto)
        dao.insert(accommodation)

        return make_response(HTTPStatus.CREATED)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.CREATED)

    except AlreadyExistsError as err:
        return make_response(
            jsonify({'message': err.message}), HTTPStatus.CONFLICT
        )


@bp.get('/<id>/')
def get_accommodation(id):
    db = get_db()
    dao = AccommodationDAO(db)
    url_param = escape(id)

    exists = dao.findBy('id', str(url_param))

    if not exists:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(exists.model_dump(), HTTPStatus.OK)


@bp.delete('/<id>/')
def delete_accommodation(id):
    db = get_db()
    dao = AccommodationDAO(db)
    url_param = escape(id)

    try:
        dao.delete(str(url_param))
        return make_response('DELETED', 200)

    except NotFoundError as err:
        return make_response({'message': err.message}, err.status)


@bp.put('/<id>/')
def update_accommodation(id):
    db = get_db()
    dao = AccommodationDAO(db)
    data = request.get_json()
    url_param = escape(id)
    try:
        accommodation = AccommodationSchema(**data)
        dao.update(url_param, accommodation)
        return 'UPDATED', 201

    except ValidationError as err:
        return make_response(jsonify({'message': err.title}), 400)

    except NotFoundError as err:
        return make_response({'message': err.message}, err.status)
