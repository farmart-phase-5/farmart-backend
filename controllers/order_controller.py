from flask import jsonify, session
from ..extensions import db
from ..models.order import Order, OrderItem
from ..models.user import User

def create_order(data):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401

    customer_id = session['user_id']
    items_data = data.get('items')

    if not items_data or not isinstance(items_data, list):
        return jsonify({'error': 'Order must contain at least one item'}), 400

    order = Order(customer_id=customer_id)
    db.session.add(order)
    db.session.flush() 

    for item in items_data:
        product_name = item.get('product_name')
        quantity = item.get('quantity')

        if not product_name or not isinstance(quantity, int):
            return jsonify({'error': 'Invalid item format'}), 400

        order_item = OrderItem(
            product_name=product_name,
            quantity=quantity,
            order_id=order.id
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify({
        'message': 'Order created successfully',
        'order_id': order.id
    }), 201


def get_orders():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'admin':
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(customer_id=user_id).all()

    result = []
    for order in orders:
        items = [{
            'product_name': item.product_name,
            'quantity': item.quantity
        } for item in order.items]

        result.append({
            'id': order.id,
            'customer_name': user.username,
            'items': items
        })

    return jsonify(result), 200


def get_order_by_id(order_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401

    user_id = session['user_id']
    user = User.query.get(user_id)
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if user.role != 'admin' and order.customer_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    items = [{
        'product_name': item.product_name,
        'quantity': item.quantity
    } for item in order.items]

    return jsonify({
        'id': order.id,
        'customer_name': user.username if user else "Unknown",
        'items': items
    }), 200
