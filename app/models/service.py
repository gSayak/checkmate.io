from . import db
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # 'video_meeting' or 'priority_dm'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))