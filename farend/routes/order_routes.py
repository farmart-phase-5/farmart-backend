'''from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from farend.controllers.order_controllers import OrderController

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    return OrderController.create_order(data)

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    return OrderController.get_orders()

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    return OrderController.get_order(order_id)

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.get_json()
    return OrderController.update_order(order_id, data)

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    return OrderController.delete_order(order_id)'''