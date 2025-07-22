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
        'quantity': order.quantity,
        'created_at': order.created_at.isoformat(),
        'farmer_notes': order.farmer_notes,
        'total_amount': order.total_amount
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
        'quantity': order.quantity,
        'created_at': order.created_at.isoformat(),
        'farmer_notes': order.farmer_notes,
        'total_amount': order.total_amount
    })

@order_routes.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json()
    new_status = data.get('status')
    notes = data.get('farmer_notes')

    if new_status:
        if new_status not in ['accepted', 'denied']:
            return jsonify({'error': 'Invalid status'}), 400
        order.status = new_status

    if notes:
        order.farmer_notes = notes

    db.session.commit()

    return jsonify({
        'message': f'Order {order.id} updated successfully',
        'updated_order': {
            'id': order.id,
            'status': order.status,
            'farmer_notes': order.farmer_notes
        }
    })


@order_routes.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get('user_id')
    animal_id = data.get('animal_id')
    status = data.get('status', 'pending')
    quantity = data.get('quantity')

    if not all([user_id, animal_id, quantity]):
        return jsonify({'error': 'user_id, animal_id, and quantity are required'}), 400

    new_order = Order(
        user_id=user_id,
        animal_id=animal_id,
        status=status,
        quantity=quantity
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        'message': 'Order created successfully',
        'order': {
            'id': new_order.id,
            'user_id': new_order.user_id,
            'animal_id': new_order.animal_id,
            'status': new_order.status,
            'quantity': new_order.quantity,
            'created_at': new_order.created_at.isoformat(),
            'farmer_notes': new_order.farmer_notes,
            'total_amount': new_order.total_amount
        }
    }), 201


@order_routes.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': f'Order with ID {order_id} has been successfully deleted'}), 200
