from app import db
from datetime import datetime 

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    user_id = id = db.Column(db.Integer, db.Foreignkey('users.id'), nullable = True)
    total_price = db.Column(db.String(10), default = 'pending')
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    user = db.relationship('User', backref = 'orders')
    items = db.relationship('OrderItem', backref = 'order', cascade = 'all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.INteger, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    animal = db.relationship('Animal')