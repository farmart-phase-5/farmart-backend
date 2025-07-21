from flask import jsonify
from extensions import db
from farend.models.payment import Payment
from farend.schema.payment_schema import validate_payment_data, serialize_payment, serialize_payments

class PaymentController:
    @staticmethod
    def create_payment(data):
        validated_data, errors = validate_payment_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        new_payment = Payment(
            order_id=validated_data['order_id'],
            user_id=validated_data['user_id'],
            amount=validated_data['amount'],
            method=validated_data.get('method', 'M-Pesa'),
            status=validated_data.get('status', 'pending')
        )
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({"message": "Payment created successfully", "payment": serialize_payment(new_payment)}), 201

    @staticmethod
    def get_payments():
        payments = Payment.query.all()
        return jsonify({"payments": serialize_payments(payments)}), 200

    @staticmethod
    def get_payment(payment_id):
        payment = Payment.query.get_or_404(payment_id)
        return jsonify({"payment": serialize_payment(payment)}), 200

    @staticmethod
    def update_payment(payment_id, data):
        payment = Payment.query.get_or_404(payment_id)
        validated_data, errors = validate_payment_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        payment.order_id = validated_data.get('order_id', payment.order_id)
        payment.user_id = validated_data.get('user_id', payment.user_id)
        payment.amount = validated_data.get('amount', payment.amount)
        payment.method = validated_data.get('method', payment.method)
        payment.status = validated_data.get('status', payment.status)
        db.session.commit()
        return jsonify({"message": "Payment updated successfully", "payment": serialize_payment(payment)}), 200

    @staticmethod
    def delete_payment(payment_id):
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Payment deleted successfully"}), 200