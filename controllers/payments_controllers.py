from flask import jsonify
from ..models.payment import Payment
from ..models.order import Order
from ..extensions import db
from datetime import datetime

def create_payment(request):
    data = request.get_json()
    order_id = data.get('order_id')
    amount = data.get('amount')
    method = data.get('method')

    if not order_id or not amount or not method:
        return jsonify({'error': 'Missing required fields'}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    payment = Payment(order_id=order_id, amount=amount, method=method)
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'id': payment.id,
        'order_id': payment.order_id,
        'amount': payment.amount,
        'method': payment.method,
        'status': payment.status,
        'paid_at': payment.paid_at.isoformat()
    }), 201

def get_payment(id):
    payment = Payment.query.get(id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    return jsonify({
        'id': payment.id,
        'order_id': payment.order_id,
        'amount': payment.amount,
        'method': payment.method,
        'status': payment.status,
        'paid_at': payment.paid_at.isoformat()
    }), 200
