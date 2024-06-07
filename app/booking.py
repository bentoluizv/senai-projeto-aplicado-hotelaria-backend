from flask import render_template
from flask import Blueprint
from markupsafe import escape

from app.data.dao.BookingDAO import BookingDAO
from app.data.database.db import get_db
from app.data.repositories.BookingRepository import BookingRepository
from app.entity.Booking import Booking


bp = Blueprint('booking', __name__, url_prefix='/')

@bp.get('/')
def booking():
    db = get_db()
    dao = BookingDAO(db)
    respository = BookingRepository(dao)
    bookings = [ guest.to_dict() for guest in respository.find_many() ]
    return render_template('index.html', rows=bookings)