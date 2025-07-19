from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from farend.controllers.payments_controllers import PaymentController

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    user_id = get_jwt_identity()
    return PaymentController.get_payments(user_id)

@payment_bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    user_id = get_jwt_identity()
    return PaymentController.create_payment(data, user_id)
