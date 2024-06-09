from flask import Blueprint, render_template

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

