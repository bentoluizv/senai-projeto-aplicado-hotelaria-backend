from flask import Blueprint, render_template
from markupsafe import escape

from app.data.dao.AccommodationDAO import AccommodationDAO
from app.data.database.db import get_db
from app.data.repositories.AccommodationRepository import AccommodationtRepository

bp = Blueprint("accommodation", __name__, url_prefix="/acomodacoes")


@bp.get("/")
def get_accommodations():
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    accommodation = [
        accommodation.to_dict() for accommodation in repository.find_many()
    ]
    return render_template("accommodations.html", rows=accommodation)


@bp.get("/cadastro/")
def new():
    return render_template("newAccommodation.html")


@bp.get("/<uuid>/")
def get_accommodation(uuid):
    url_param = escape(uuid)
    db = get_db()
    dao = AccommodationDAO(db)
    repository = AccommodationtRepository(dao)
    accommodation = repository.findBy("uuid", str(url_param))
    return render_template(
        "updateAccommodation.html", accommodation=accommodation.to_dict()
    )
