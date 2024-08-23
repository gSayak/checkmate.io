from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .expert import Expert
from .service import Service
from .booking import Booking
from .message import Message