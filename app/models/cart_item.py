from app import db
from app.models.animal_model import Animal
from app.models.user_model import User

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

   
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True, cascade='all, delete-orphan'))
    animal = db.relationship('Animal', backref=db.backref('cart_items', lazy=True, cascade='all, delete-orphan'))


    def __repr__(self):
        return (
            f"<CartItem id={self.id} user_id={self.user_id} "
            f"cart_id={self.cart_id} animal_id={self.animal_id} quantity={self.quantity}>"
        )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "cart_id": self.cart_id,
            "animal_id": self.animal_id,
            "animal_name": self.animal.name if self.animal else None,
            "quantity": self.quantity,
            "added_at": self.added_at.isoformat() if self.added_at else None
        }
