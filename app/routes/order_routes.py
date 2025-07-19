from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.order_controllers import OrderController

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    return OrderController.get_orders(user_id)

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    return OrderController.create_order(data, user_id)

@order_bp.route('/orders/<int:order_id>', methods=['PATCH'])
@jwt_required()
def update_order(order_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    return OrderController.update_order(order_id, data, user_id)

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    user_id = get_jwt_identity()
    return OrderController.delete_order(order_id, user_id)
