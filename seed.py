from app import create_app
from extension import db
from models.farmer import Farmer
from models.animals import Animals

app = create_app()

with app.app_context():
    # Drop and recreate all tables (optional — only if you want to reset everything)
    db.drop_all()
    db.create_all()

    # Seed Farmers
    farmer1 = Farmer(name="John Doe", location="Nakuru", email="john@example.com")
    farmer2 = Farmer(name="Alice Wambui", location="Nyeri", email="alice@example.com")

    # Seed Animals
    animal1 = Animals(name="Cow", age=5, species="Friesian", farmer=farmer1)
    animal2 = Animals(name="Goat", age=2, species="Kalahari", farmer=farmer2)

    # Add to session and commit
    db.session.add_all([farmer1, farmer2, animal1, animal2])
    db.session.commit()

    print("🌱 Seed data added!")

