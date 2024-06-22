from http import HTTPStatus

from flask import Blueprint, jsonify, make_response
from pydantic import ValidationError

from app.data.dao.AmenitieDAO import AmenitieDAO
from app.data.database.sqlite.db import get_db

bp = Blueprint('api_amenities', __name__, url_prefix='/amenities')


@bp.get('/')
@bp.get('')
def get_all_amenities():
    try:
        db = get_db()
        dao = AmenitieDAO(db)
        amenities = [amenitie.model_dump() for amenitie in dao.find_many()]
        return jsonify(amenities)

    except ValidationError as err:
        return make_response(err.json(), HTTPStatus.UNPROCESSABLE_ENTITY)
