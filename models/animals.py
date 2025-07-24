from farend.extensions import db

from sqlalchemy.orm import relationship


class Animals(db.Model):

    __tablename__ = 'animals'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    image_url = db.Column(db.String)
    available = db.Column(db.Boolean, default=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id')) 

    owner = db.relationship("Farmer", back_populates="my_animals")

    def __repr__(self):
     return f"<Animals {self.name}>"


