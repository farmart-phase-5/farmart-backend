from flask import request, jsonify
from app.models.payment import Payment
from app import db
from app.schema.payment_schema import PaymentSchema

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

def get_payments():
    payments = Payment.query.all()
    return jsonify(payments_schema.dump(payments)), 200

def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment_schema.dump(payment)), 200

def create_payment():
    data = request.get_json()
    errors = payment_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_payment = Payment(
        amount=data['amount'],
        status=data['status'],
        order_id=data['order_id'],
        user_id=data['user_id']
    )

    db.session.add(new_payment)
    db.session.commit()
    return jsonify(payment_schema.dump(new_payment)), 201

def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()

    errors = payment_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    payment.amount = data.get('amount', payment.amount)
    payment.status = data.get('status', payment.status)
    payment.order_id = data.get('order_id', payment.order_id)
    payment.user_id = data.get('user_id', payment.user_id)

    db.session.commit()
    return jsonify(payment_schema.dump(payment)), 200

def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({"message": "Payment deleted"}), 204
