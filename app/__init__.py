from flask import Flask
from .models import db
from .api import register_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.qqcnutlzmbkfqcbipocn:sayakghosh22@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        register_routes(app)
        db.create_all()  # Creates the tables if they don't exist

    return app