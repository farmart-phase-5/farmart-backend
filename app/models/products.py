from app import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable = False)
    stock = db.Column(db.Integer, default = 0)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'farmer_id': self.farmer_id
        }