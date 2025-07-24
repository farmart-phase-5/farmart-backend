#from sqlalchemy.orm import relationship
#from flask_jwt_extended import JWTManager
#from extension import db


#class Farmer(db.Model):
   # __tablename__ = 'farmers'

    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(100), nullable=False)
    #phone_number = db.Column(db.String(20), nullable=False, unique=True)
    #email = db.Column(db.String(120), nullable=True, unique=True)

  
    #my_animals = db.relationship("Animals", back_populates="owner", lazy=True)



    #def __repr__(self):
     #   return f"<Farmer {self.name}>" 