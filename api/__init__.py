import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask import Flask
from .models import db
from .api import register_routes

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    db.init_app(app)
    JWTManager(app)
    with app.app_context():
        register_routes(app)
        db.create_all()  # Creating the tables if they dont exist
    return app