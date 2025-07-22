from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)

    
    farmer_notes = db.Column(db.Text)  

    animal = db.relationship('Animal', backref='orders', lazy=True)


    @property
    def total_amount(self):
        return self.quantity * self.animal.price if self.animal else 0
