import os

from flask import Flask, render_template
from flask_cors import CORS

from . import accommodation, booking, guest
from .data.database.sqlite import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    app.register_blueprint(guest.bp)
    app.register_blueprint(accommodation.bp)
    app.register_blueprint(booking.bp)

    return app
