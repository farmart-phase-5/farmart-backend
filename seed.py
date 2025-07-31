from app import app
from config import db
from models import User, Animal, CartItem, Order, OrderItem

with app.app_context():
    db.create_all()
    print("🌱 Seeding database...")

    
    OrderItem.query.delete()
    Order.query.delete()
    CartItem.query.delete()
    Animal.query.delete()
    User.query.delete()
    db.session.commit()


    users = [
        User(username="farmer_john", email="john@farmart.com", role="farmer"),
        User(username="farmer_jane", email="jane@farmart.com", role="farmer"),
        User(username="buyer_mike", email="mike@buyer.com", role="buyer"),
        User(username="buyer_susan", email="susan@buyer.com", role="buyer")
    ]
    for user in users:
        user.password_hash = "password123"
        db.session.add(user)
    db.session.commit()

    
    animals = [
        Animal(name="Daisy", type="cow", breed="Friesian", price=20000, image="https://example.com/cow.jpg", farmer_id=users[0].id),
        Animal(name="Billy", type="goat", breed="Boer", price=7000, image="https://example.com/goat.jpg", farmer_id=users[0].id),
        Animal(name="Clucky", type="chicken", breed="Kienyeji", price=1200, image="https://example.com/chicken.jpg", farmer_id=users[1].id),
        Animal(name="Wooly", type="sheep", breed="Dorper", price=15000, image="https://example.com/sheep.jpg", farmer_id=users[1].id),
    ]
    db.session.add_all(animals)
    db.session.commit()

    
    cart_items = [
        CartItem(user_id=users[2].id, animal_id=animals[0].id, quantity=1),
        CartItem(user_id=users[3].id, animal_id=animals[2].id, quantity=3),
    ]
    db.session.add_all(cart_items)
    db.session.commit()


    order1 = Order(user_id=users[2].id, status="pending", total_price=animals[0].price * 1)
    db.session.add(order1)
    db.session.flush()  
    db.session.add(OrderItem(order_id=order1.id, animal_id=animals[0].id, quantity=1))

    order2 = Order(user_id=users[3].id, status="delivered", total_price=animals[2].price * 3)
    db.session.add(order2)
    db.session.flush()
    db.session.add(OrderItem(order_id=order2.id, animal_id=animals[2].id, quantity=3))

    db.session.commit()
    print("✅ Done seeding!")
