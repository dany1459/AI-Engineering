from email.policy import default

from pytz import timezone
from utils.db import db
from sqlalchemy.sql import func
import uuid

class User(db.Model):
    user_id = db.Column(db.String(32), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

    def to_json(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': str(self.created_at)
        }
