from datetime import datetime
from farend.models import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("Client", back_populates="orders")
    product = db.relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<Order #{self.id} - Client {self.client_id} | Product {self.product_id} | Qty {self.quantity}>"
