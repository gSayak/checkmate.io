from . import db
from datetime import datetime, timezone
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))