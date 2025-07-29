from flask import jsonify, g
from ..extensions import db
from ..models.order import Order, OrderItem
from ..models.user import User

def create_order(data):
    if not getattr(g, 'user_id', None):
        return jsonify({'error': 'Authentication required'}), 401

    customer_id = g.user_id
    items_data = data.get('items')

    if not items_data or not isinstance(items_data, list):
        return jsonify({'error': 'Order must contain at least one item'}), 400

    if len(items_data) == 0:
        return jsonify({'error': 'Order must contain at least one item'}), 400

    total_amount = 0.0

    for item in items_data:
        product_name = item.get('product_name')
        quantity = item.get('quantity')
        price = item.get('price')

        if not product_name or not isinstance(quantity, int) or quantity <= 0:
            return jsonify({'error': 'Each item must have a valid product_name and positive integer quantity'}), 400

        if not isinstance(price, (int, float)) or price < 0:
            return jsonify({'error': 'Each item must have a valid non-negative price'}), 400

        total_amount += quantity * price

    order = Order(user_id=customer_id, total=total_amount, status='pending')
    db.session.add(order)
    db.session.flush() 

    for item in items_data:
        order_item = OrderItem(
            product_name=item['product_name'],
            quantity=item['quantity'],
            price=item['price'],
            order_id=order.id
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify({
        'message': 'Order created successfully',
        'order_id': order.id,
        'total': total_amount
    }), 201


def get_orders():
    if not getattr(g, 'user_id', None):
        return jsonify({'error': 'Authentication required'}), 401

    user_id = g.user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'admin':
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=user_id).all()

    result = []
    for order in orders:

        items = [{
            'product_name': item.product_name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.order_items]

        customer = User.query.get(order.user_id)
        customer_name = customer.username if customer else "Unknown"

        result.append({
            'id': order.id,
            'customer_name': customer_name,
            'total': order.total,
            'status': order.status,
            'items': items
        })

    return jsonify(result), 200


def get_order_by_id(order_id):
    
    if not getattr(g, 'user_id', None):
        return jsonify({'error': 'Authentication required'}), 401

    user_id = g.user_id
    user = User.query.get(user_id)
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if user.role != 'admin' and order.user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    items = [{
        'product_name': item.product_name,
        'quantity': item.quantity,
        'price': item.price
    } for item in order.order_items]

    customer = User.query.get(order.user_id)
    customer_name = customer.username if customer else "Unknown"

    return jsonify({
        'id': order.id,
        'customer_name': customer_name,
        'total': order.total,
        'status': order.status,
        'items': items
    }), 200
