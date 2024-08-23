from . import db
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('services.id'), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'completed', 'expired'
    booking_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expiry_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))