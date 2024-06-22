from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.BookingDAO import BookingDAO
from app.data.dao.GuestDAO import GuestDAO
from app.data.database.sqlite.db import get_db
from app.data.repository.BookingRepository import BookingRepository
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError

bp = Blueprint('api_booking', __name__, url_prefix='/reservas')


@bp.get('')
@bp.get('/')
def get_bookings():
    try:
        db = get_db()
        booking_dao = BookingDAO(db)
        guest_dao = GuestDAO(db)
        accommodation_dao = AccommodationDAO(db)
        repository = BookingRepository(
            booking_dao, accommodation_dao, guest_dao
        )
        bookings_db = repository.find_many()
        bookings = [booking.model_dump() for booking in bookings_db]

        return jsonify(bookings)

    except ValidationError as err:
        return make_response(err.json, HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.get('/<uuid>')
@bp.get('/<uuid>/')
def get_accommodation(uuid):
    try:
        db = get_db()
        booking_dao = BookingDAO(db)
        guest_dao = GuestDAO(db)
        accommodation_dao = AccommodationDAO(db)
        repository = BookingRepository(
            booking_dao, accommodation_dao, guest_dao
        )
        url_param = str(escape(uuid))

        booking = repository.find(url_param)
        return jsonify(booking.model_dump())

    except NotFoundError as err:
        return make_response(jsonify({'message': err.message}), 404)


@bp.post('/cadastro')
@bp.post('/cadastro/')
def create_booking():
    try:
        db = get_db()
        booking_dao = BookingDAO(db)
        guest_dao = GuestDAO(db)
        accommodation_dao = AccommodationDAO(db)
        repository = BookingRepository(
            booking_dao, accommodation_dao, guest_dao
        )

        data = request.get_json()

        repository.create(data)

        return make_response('CREATED', HTTPStatus.CREATED)

    except AlreadyExistsError as err:
        return make_response(err.json(), err.status_code)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)


@bp.put('/<uuid>')
@bp.put('/<uuid>/')
def update_accommodation(uuid):
    try:
        db = get_db()
        booking_dao = BookingDAO(db)
        guest_dao = GuestDAO(db)
        accommodation_dao = AccommodationDAO(db)
        repository = BookingRepository(
            booking_dao, accommodation_dao, guest_dao
        )

        data = request.get_json()

        repository.update(data)
        return make_response({}, HTTPStatus.NO_CONTENT)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)

    except NotFoundError as err:
        return make_response(err.json(), HTTPStatus.NOT_FOUND)


@bp.delete('/<uuid>/')
def delete_accommodation(uuid):
    try:
        db = get_db()
        booking_dao = BookingDAO(db)
        guest_dao = GuestDAO(db)
        accommodation_dao = AccommodationDAO(db)
        repository = BookingRepository(
            booking_dao, accommodation_dao, guest_dao
        )
        url_param = str(escape(uuid))

        repository.delete(url_param)
        return make_response({}, HTTPStatus.NO_CONTENT)

    except NotFoundError as err:
        return make_response(err.json(), err.status_code)
