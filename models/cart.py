from farend.extensions import db

from datetime import datetime

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.String, default='open')  # open, checked_out
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('CartItem', back_populates='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=1)

    cart = db.relationship('Cart', back_populates='items')
