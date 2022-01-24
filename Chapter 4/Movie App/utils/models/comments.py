from utils.db import db
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Comments(db.Model):
    comment_id = db.Column(db.String(32), primary_key=True, default=generate_uuid, nullable=False, unique=True)
    movie_id = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def to_json(self):
        return {
            'comment_id': self.comment_id,
            'movie_id': self.movie_id,
            'text': self.text,
            'created_at': str(self.created_at)
        }