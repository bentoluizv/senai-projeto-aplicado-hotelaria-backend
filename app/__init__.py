"""Flask Application Factory"""

import os
from flask import Flask
from flask import render_template
from .data.database import db
from flask import request

from app.data.dao.GuestDAO import GuestDAO
from app.data.database.db import get_db
from markupsafe import escape

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
    @app.get('/index')
    def index():
        return render_template('index.html')
    
    @app.get('/cadastroHospedes')
    def cadastroHospedes():               
        return render_template('cadastroHospedes.html')  
    
    @app.get('/cadastroReservas')
    def cadastroReservas():               
        return render_template('cadastroReservas.html')
    
    
   

    @app.get('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    from . import  guests
    app.register_blueprint(guests.bp)


    '''
     @app.get('/list')
    def list():               
        return render_template('list.html')  
    '''

    @app.get('/list')
    def list():
            
        # Connect to the SQLite3 datatabase and 
        # SELECT  Rows from the guest table.
        db = get_db()
        guest_dao = GuestDAO(db)
        rows = guest_dao.find_many()

        
        # Send the results of the SELECT to the list.html page
        return render_template("list.html", rows=rows)   
    
        
    @app.post('/deletar')
    def deletar():       
        db = get_db()
             
      
        rowid = request.form['document']
        cur = db.cursor()
        cur.execute('DELETE FROM guest WHERE document= "' + rowid +'"')
        db.commit()
        msg = "Record successfully deleted from the database"
        return list() 
     
    
             


    return app
