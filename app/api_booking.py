import click
from flask import Blueprint, abort, jsonify, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.BookingDAO import BookingDAO
from app.data.database.db import get_db
from app.data.repositories.BookingRepository import BookingRepository
from app.entity.Booking import Booking


bp = Blueprint('api_booking', __name__, url_prefix='/api/reservas')


@bp.get('')
def get_bookings():
    db = get_db()
    dao = BookingDAO(db)
    respository = BookingRepository(dao)

    try:
        bookings = [ booking.to_dict() for booking in respository.find_many() ]
        return jsonify(bookings)

    except ValidationError as err:
        abort(500)


@bp.post('/cadastro')
def create_booking():
    booking_json = request.get_json()

    if booking_json is None:
        abort(400)

    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)

    try:
        booking =  Booking.from_dict(booking_json)
        repository.insert(booking)
        return 'CREATED', 201

    except ValueError as e:
        click.echo(e)
        abort(400)


@bp.get('/<uuid>')
def get_accommodation(uuid):
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    url_param = escape(uuid)

    try:
        booking = repository.find(str(url_param))
        return booking.to_json()

    except ValueError:
        abort(404)


@bp.delete('/<uuid>')
def delete_accommodation(uuid):
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    url_param = escape(uuid)

    try:
        repository.delete(str(url_param))
        return 'DELETED', 200

    except ValueError:
        abort(404)


@bp.put('')
def update_accommodation():
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    booking_json  = request.get_json()

    try:
        booking = Booking.from_dict(booking_json)
        repository.update(booking)
        return "UPDATED", 201

    except ValidationError as err:
        click.echo(err)
        abort(400)

    except ValueError as err:
        click.echo(err)
        abort(404)