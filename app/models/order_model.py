from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Add this if you want to track the user
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    farmer_notes = db.Column(db.Text, nullable=True)

    order_items = db.relationship('OrderItem', back_populates='order')

    @property
    def total_amount(self):
        # Sum price * quantity for each order item
        return sum(item.animal.price * item.quantity for item in self.order_items)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "farmer_id": self.farmer_id,
            "status": self.status,
            "farmer_notes": self.farmer_notes,
            "total_amount": self.total_amount,
            "order_items": [item.to_dict() for item in self.order_items]
        }