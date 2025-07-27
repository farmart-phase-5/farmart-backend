from flask import jsonify
from extensions import db
from models.order import Order, OrderItem

def create_order(data):
    customer_name = data.get('customer_name')
    items_data = data.get('items', [])

    if not customer_name or not items_data:
        return jsonify({'error': 'Missing order data'}), 400

    order = Order(customer_name=customer_name)
    db.session.add(order)
    db.session.flush()

    for item in items_data:
        order_item = OrderItem(
            product_name=item['product_name'],
            quantity=item['quantity'],
            order=order
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'message': 'Order created', 'order_id': order.id}), 201

def get_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        items = [{'product_name': i.product_name, 'quantity': i.quantity} for i in order.items]
        result.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'items': items
        })
    return jsonify(result), 200
