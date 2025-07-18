from flask import Blueprint, request, jsonify
from app.models import db, Order, Animal

order_routes = Blueprint('order_routes', __name__)


@order_routes.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'user_id': order.user_id,
            'animal_id': order.animal_id,
            'status': order.status,
            'created_at': order.created_at.isoformat()
        })
    return jsonify(result)


@order_routes.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    data = request.get_json()
    status = data.get('status')
    if status not in ['accepted', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.status = status
    db.session.commit()
    return jsonify({'message': f'Order {order_id} status updated to {status}'})


@order_routes.route('/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': f'Animal {animal_id} deleted successfully'})
