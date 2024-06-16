from click import echo
from flask import Blueprint, abort, jsonify, make_response, request
from markupsafe import escape
from pydantic import ValidationError

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.dao.BookingDAO import BookingDAO
from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository
from app.data.repositories.BookingRepository import BookingRepository
from app.data.repositories.GuestRepository import GuestRepository
from app.entity.Booking import Booking
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError

bp = Blueprint("api_booking", __name__, url_prefix="/api/reservas")


@bp.get("")
def get_bookings():
    db = get_db()
    dao = BookingDAO(db)
    respository = BookingRepository(dao)

    try:
        bookings = [booking.to_dict() for booking in respository.find_many()]
        return make_response(jsonify(bookings), 200)

    except ValidationError as err:
        echo(err)
        return make_response(jsonify({"message": err.title}), 500)


@bp.post("/cadastro")
def create_booking():
    try:
        booking_json = request.get_json()
        if not booking_json:
            abort(400)

        db = get_db()

        bookingDAO = BookingDAO(db)
        bookingRepository = BookingRepository(bookingDAO)

        guestDAO = GuestDAO(db)
        guestRepository = GuestRepository(guestDAO)

        accommodationDAO = AccommodationDAO(db)
        accommodationRepository = AccommodationtRepository(accommodationDAO)

        guest = guestRepository.findBy("document", booking_json["guest_document"])
        accommodation = accommodationRepository.findBy(
            "id", booking_json["accommodation_id"]
        )

        booking_data = {
            "check_in": booking_json["check_in"],
            "check_out": booking_json["check_out"],
            "guest": guest,
            "accommodation": accommodation,
        }

        booking = Booking.from_dict(booking_data)
        bookingRepository.insert(booking)
        return make_response("CREATED", 201)

    except AlreadyExistsError as err:
        echo(err)
        return make_response(jsonify({"message": err.message}), err.status)

    except ValidationError as err:
        echo(err)
        return make_response(jsonify({"message": err.title}), 400)


@bp.get("/<uuid>")
def get_accommodation(uuid):
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    url_param = escape(uuid)

    try:
        booking = repository.findBy("uuid", str(url_param))
        return make_response(booking.to_json(), 200)

    except NotFoundError as err:
        echo(err)
        return make_response(jsonify({"message": err.message}), 404)


@bp.delete("/<uuid>")
def delete_accommodation(uuid):
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    url_param = escape(uuid)

    try:
        repository.delete(str(url_param))
        return make_response("DELETED", 200)

    except NotFoundError as err:
        echo(err)
        return make_response(jsonify({"message": err.message}), err.status)


@bp.put("")
def update_accommodation():
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    booking_json = request.get_json()

    try:
        booking = Booking.from_dict(booking_json)
        repository.update(booking)
        return make_response("UPDATED", 200)

    except ValidationError as err:
        echo(err)
        return make_response(jsonify({"message": err.title}), 400)

    except NotFoundError as err:
        echo(err)
        return make_response(jsonify({"message": err.message}), err.status)
