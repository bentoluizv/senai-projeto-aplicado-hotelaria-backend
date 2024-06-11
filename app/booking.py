from flask import Blueprint, render_template
from markupsafe import escape

from app.data.dao.BookingDAO import BookingDAO
from app.data.database.db import get_db
from app.data.repositories.BookingRepository import BookingRepository

bp = Blueprint("booking", __name__, url_prefix="/reservas")


@bp.get("/")
def booking():
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)
    bookings = [booking.to_dict() for booking in repository.find_many()]
    print(bookings)  # Adicione este print para verificar os dados
    return render_template("index.html", rows=bookings)

@bp.get("/cadastro/")
def cadastro():
    return render_template("newBooking.html")    

@bp.get("/<resource>/<guest_document>")
def get_booking(resource, guest_document):
    url_param = escape(guest_document)
    resource_param = escape(resource)
    print("Resource:", resource_param)
    print("Document:", url_param)
    db = get_db()
    dao = BookingDAO(db)
    repository = BookingRepository(dao)

    if resource_param == 'reserva':
        bookings = repository.findBy("uuid", str(url_param))
    elif resource_param == 'hospede':
        bookings = repository.findBy("document", str(url_param))
    else:
        bookings = []

    return render_template("index.html", rows=bookings)

    




