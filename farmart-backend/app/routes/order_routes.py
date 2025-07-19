from flask import Blueprint, request, jsonify
from app.models import Order, db  

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_list = [{
        'id': order.id,
        'user_id': order.user_id,
        'animal_id': order.animal_id,
        'status': order.status,
        'created_at': order.created_at.isoformat()
    } for order in orders]
    return jsonify(order_list)

@order_routes.route('/orders/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'animal_id': order.animal_id,
        'status': order.status,
        'created_at': order.created_at.isoformat()
    })

@order_routes.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['accepted', 'denied']:
        return jsonify({'error': 'Invalid status'}), 400

    order.status = new_status
    db.session.commit()

    return jsonify({'message': f'Order {order.id} status updated to {new_status}'})
