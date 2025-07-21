import sys
import os
from datetime import datetime, timezone

# Fix import path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Farmer, Animal, Order  

app = create_app()

with app.app_context():
    
    db.session.query(Order).delete()
    db.session.query(Animal).delete()
    db.session.query(Farmer).delete()

 
    farmer = Farmer(username="testfarmer", password="hashedpassword")
    db.session.add(farmer)
    db.session.commit()

    animal1 = Animal(id=101, name="Cow", breed="Friesian", age=2, price=1200, farmer_id=farmer.id)
    animal2 = Animal(id=102, name="Goat", breed="Boer", age=1, price=400, farmer_id=farmer.id)
    animal3 = Animal(id=103, name="Sheep", breed="Dorper", age=3, price=500, farmer_id=farmer.id)

    db.session.add_all([animal1, animal2, animal3])
    db.session.commit()

    
    order1 = Order(user_id=1, animal_id=101, status='pending', created_at=datetime.now(timezone.utc))
    order2 = Order(user_id=2, animal_id=102, status='pending', created_at=datetime.now(timezone.utc))
    order3 = Order(user_id=3, animal_id=103, status='pending', created_at=datetime.now(timezone.utc))

    db.session.add_all([order1, order2, order3])
    db.session.commit()

    print(" Seeded farmers, animals, and orders successfully.")
