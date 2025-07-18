from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order
from app import db

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user = get_jwt_identity()
    data = request.get_json()
    order = Order(user_id=user['id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@order_bp.route('/orders/<int:id>', methods=['PATCH'])
@jwt_required()
def update_order(id):
    user = get_jwt_identity()
    order = Order.query.get_or_404(id)

    if user['role'] not in ['admin', 'farmer']:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify(order.to_dict()), 200

@order_bp.route('/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    user = get_jwt_identity()
    order = Order.query.get_or_404(id)
    if user['id'] != order.user_id and user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200
