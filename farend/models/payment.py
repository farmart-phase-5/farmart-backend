from extensions import db
from datetime import datetime
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)  # e.g. 'MPESA', 'CARD'
    status = db.Column(db.String(20), default='pending')
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='payment')
