from datetime import datetime
import app

db = app.db

class Order(db.Model):
    __tablename__ = 'farend_orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Changed from client_name
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')
    
    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }