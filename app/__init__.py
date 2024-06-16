"""Flask Application Factory"""

import os

from flask import Flask, json, render_template
from flask_cors import CORS

from .data.database.sqlite3 import db


def create_app(test_config=None):
    """create and config the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    @app.errorhandler(404)
    def resource_not_found(e):
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(409)
    def resource_already_exists(e):
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(400)
    def bad_request(e):
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/hello")
    def hello():
        return "Hello, World!"

    db.init_app(app)

    from . import api_guest, guests

    app.register_blueprint(guests.bp)
    app.register_blueprint(api_guest.bp)

    from . import accommodations, api_accommodations

    app.register_blueprint(accommodations.bp)
    app.register_blueprint(api_accommodations.bp)

    from . import api_amenities

    app.register_blueprint(api_amenities.bp)

    from . import api_booking, booking

    app.register_blueprint(booking.bp)
    app.register_blueprint(api_booking.bp)

    return app
