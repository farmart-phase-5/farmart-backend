from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from farend.controllers.payments_controllers import PaymentController

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    return PaymentController.create_payment(data)

@payment_bp.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    return PaymentController.get_payments()

@payment_bp.route('/payments/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    return PaymentController.get_payment(payment_id)

@payment_bp.route('/payments/<int:payment_id>', methods=['PUT'])
@jwt_required()
def update_payment(payment_id):
    data = request.get_json()
    return PaymentController.update_payment(payment_id, data)

@payment_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete_payment(payment_id):
    return PaymentController.delete_payment(payment_id)