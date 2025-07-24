from farend.models.payment import Payment
from farend.models.user import User


def validate_payment_data(data):
    errors = []
    validated_data = {}

    
    if 'user_id' not in data or not isinstance(data['user_id'], int):
        errors.append("User ID is required and must be an integer.")
    else:
        if not User.query.get(data['user_id']):
            errors.append("Invalid user_id: User does not exist.")
        validated_data['user_id'] = data['user_id']

    if 'amount' not in data or not isinstance(data['amount'], (int, float)) or data['amount'] < 0:
        errors.append("Amount is required and must be a non-negative number.")
    else:
        validated_data['amount'] = data['amount']

    if 'method' in data:
        validated_data['method'] = data.get('method', 'M-Pesa')

    if 'status' in data and data['status'] not in ['pending', 'completed', 'failed']:
        errors.append("Status must be 'pending', 'completed', or 'failed'.")
    else:
        validated_data['status'] = data.get('status', 'pending')

    return validated_data, errors

def serialize_payment(payment):
    return {
        'id': payment.id,
      '''  'order_id': payment.order_id,'''
        'user_id': payment.user_id,
        'amount': float(payment.amount),
        'method': payment.method,
        'status': payment.status,
        'created_at': payment.created_at.isoformat() if payment.created_at else None
    }

def serialize_payments(payments):
    return [serialize_payment(payment) for payment in payments]