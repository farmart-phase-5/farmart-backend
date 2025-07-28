from app import db
from sqlalchemy import Index, UniqueConstraint

class Animal(db.Model):
    __tablename__ = 'animals'
    __table_args__ = (
        UniqueConstraint('name', 'farmer_id', name='uq_animal_farmer'),  
        Index('idx_animal_breed', 'breed'), 
        Index('idx_animal_farmer', 'farmer_id')  
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False, index=True) 
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)

   
    order_items = db.relationship('OrderItem', back_populates='animal', cascade='all, delete-orphan')

    def to_dict(self, include_orders=False):
        """Enhanced with optional relationship control"""
        data = {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'age': self.age,
            'price': float(self.price),  # Convert Numeric to float for JSON
            'farmer_id': self.farmer_id
        }
        if include_orders:
            data['order_items'] = [item.to_dict() for item in self.order_items]
        return data

    def __repr__(self):
        return f'<Animal {self.id}: {self.name} ({self.breed})>'