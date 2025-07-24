from farend.extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    '''order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)'''
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), default='M-Pesa')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
        '''    'order_id': self.order_id,'''
            'user_id': self.user_id,
            'amount': self.amount,
            'method': self.method,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
