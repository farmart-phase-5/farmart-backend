from farend import db
from . import app
from farend.models.user import User
from farend.models.products import Product
from farend.models.order import Order
from farend.models.payment import Payment
from datetime import datetime

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(
        username="admin",
        email="admin@farmart.com",
        role="admin"
    )
    admin.set_password("adminpass")

    client = User(
        username="johndoe",
        email="john@client.com",
        role="client"
    )
    client.set_password("client123")

    farmer = User(
        username="maryfarmer",
        email="mary@farmart.com",
        role="farmer"
    )
    farmer.set_password("farmerpass")

    db.session.add_all([admin, client, farmer])
    db.session.commit()

    product1 = Product(
        name="Organic Tomatoes",
        description="Fresh organic tomatoes",
        price=120.0,
        quantity_available=100,
        farmer_id=farmer.id
    )

    product2 = Product(
        name="Free-Range Eggs",
        description="Eggs from free-range chickens",
        price=300.0,
        quantity_available=50,
        farmer_id=farmer.id
    )

    db.session.add_all([product1, product2])
    db.session.commit()

    order1 = Order(
        client_id=client.id,
        product_id=product1.id,
        quantity=5,
        status="pending"
    )

    db.session.add(order1)
    db.session.commit()

    payment1 = Payment(
        order_id=order1.id,
        user_id=client.id,
        amount=product1.price * order1.quantity, 
        status="paid",
        paid_at=datetime.utcnow()
    )

    db.session.add(payment1)
    db.session.commit()

    print("Database seeded successfully.")
