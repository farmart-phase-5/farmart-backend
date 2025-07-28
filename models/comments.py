from extensions import db
from datetime import datetime

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key  = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable = False)
    created_at =db.Column(db.DateTime, default = datetime.utcnow)

    user = db.relationship('User', backref='comments')