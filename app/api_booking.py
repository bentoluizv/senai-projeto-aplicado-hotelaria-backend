from http import HTTPStatus

from flask import Blueprint, abort, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.BookingDAO import BookingDAO
from app.data.dao.GuestDAO import GuestDAO
from app.data.database.sqlite.db import get_db
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError
from app.schemas.BookingSchema import BookingSchema

bp = Blueprint('api_booking', __name__, url_prefix='/api/reservas')


@bp.get('/')
def get_bookings():
    try:
        db = get_db()
        dao = BookingDAO(db)
        bookings = dao.find_many()

        return jsonify(bookings)

    except ValidationError as err:
        return make_response(err.json, HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.post('/cadastro/')
def create_booking():
    try:
        booking_json = request.get_json()

        if not booking_json:
            abort(400)

        db = get_db()

        bookingDAO = BookingDAO(db)
        guestDAO = GuestDAO(db)
        accommodatonDAO = AccommodationDAO(db)

        return make_response(jsonify(result), 201)

    except AlreadyExistsError as err:
        return make_response(jsonify({'message': err.message}), err.status)

    except ValidationError as err:
        return make_response(jsonify({'message': err.errors}), 400)


@bp.get('/<uuid>/')
def get_accommodation(uuid):
    try:
        db = get_db()
        dao = BookingDAO(db)
        repository = BookingRepository(dao)
        url_param = str(escape(uuid))

        result = find_booking_by(
            repository, {'key': 'uuid', 'value': url_param}
        )
        return jsonify(result)

    except NotFoundError as err:
        return make_response(jsonify({'message': err.message}), 404)


@bp.delete('/<uuid>/')
def delete_accommodation(uuid):
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    url_param = escape(uuid)

    try:
        repository.delete(str(url_param))
        return make_response('DELETED', 200)

    except NotFoundError as err:
        return make_response(jsonify({'message': err.message}), err.status)


@bp.put('/')
def update_accommodation():
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    booking_json = request.get_json()

    try:
        booking = BookingSchema(**booking_json)
        repository.update(booking)
        return make_response('UPDATED', 200)

    except ValidationError as err:
        return make_response(jsonify({'message': err.title}), 400)

    except NotFoundError as err:
        return make_response(jsonify({'message': err.message}), err.status)
