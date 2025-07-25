from app import db

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    price = db.Column(db.Float)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)


