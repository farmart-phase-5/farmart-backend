from datetime import datetime
import app

db = app.db

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key  = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable = False)
    created_at =db.Column(db.DateTime, default = datetime.utcnow)

    user = db.relationship('User', backref='comments')
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'username': self.user.username if self.user else None
        }