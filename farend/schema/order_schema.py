from farend.models.order import Order
from farend.models.user import User
from farend.models.products import Product

def validate_order_data(data):
    errors = []
    validated_data = {}

    if 'user_id' not in data or not isinstance(data['user_id'], int):
        errors.append("User ID is required and must be an integer.")
    else:
        if not User.query.get(data['user_id']):
            errors.append("Invalid user_id: User does not exist.")
        validated_data['user_id'] = data['user_id']

    if 'product_id' not in data or not isinstance(data['product_id'], int):
        errors.append("Product ID is required and must be an integer.")
    else:
        if not Product.query.get(data['product_id']):
            errors.append("Invalid product_id: Product does not exist.")
        validated_data['product_id'] = data['product_id']

    if 'quantity' not in data or not isinstance(data['quantity'], int) or data['quantity'] < 1:
        errors.append("Quantity is required and must be a positive integer.")
    else:
        validated_data['quantity'] = data['quantity']

    if 'total_price' not in data or not isinstance(data['total_price'], (int, float)) or data['total_price'] < 0:
        errors.append("Total price is required and must be a non-negative number.")
    else:
        validated_data['total_price'] = data['total_price']

    if 'status' in data and data['status'] not in ['Pending', 'Confirmed', 'Cancelled', 'Completed']:
        errors.append("Status must be 'Pending', 'Confirmed', 'Cancelled', or 'Completed'.")
    else:
        validated_data['status'] = data.get('status', 'Pending')

    return validated_data, errors

def serialize_order(order):
    return {
        'id': order.id,
        'user_id': order.user_id,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'total_price': float(order.total_price),
        'status': order.status,
        'created_at': order.created_at.isoformat() if order.created_at else None
    }

def serialize_orders(orders):
    return [serialize_order(order) for order in orders]