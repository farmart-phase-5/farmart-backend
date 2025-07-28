from app import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    cart_items = db.relationship(
        'CartItem',
        backref='parent_cart',  
        lazy=True,
        cascade='all, delete-orphan'
    )

    
    user = db.relationship(
        'User',
        backref=db.backref('carts', lazy=True)
    )

    def __repr__(self):
        return f"<Cart id={self.id} user_id={self.user_id}>"

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.serialize() for item in self.cart_items]
        }
