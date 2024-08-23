import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask import Flask
from api.models import db
from api import register_routes

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
db.init_app(app)
JWTManager(app)
with app.app_context():
    register_routes(app)
    db.create_all() 

if __name__ == "__main__":
 # Creating the tables if they dont exist
    app.run(host="0.0.0.0", port=5001, debug=True)