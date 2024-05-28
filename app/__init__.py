"""Flask Application Factory"""

import os
from flask import Flask
from flask import render_template
from .data.database import db


def create_app(test_config=None):
    """create and config the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    from . import  guests
    from . import  api_guest
    app.register_blueprint(guests.bp)
    app.register_blueprint(api_guest.bp)
    from . import  acomodacoes
    app.register_blueprint(acomodacoes.bp)


    return app
