from flask import request, jsonify
from app.models.order import Order
from app import db
from app.schema.order_schema import OrderSchema

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders)), 200

def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order_schema.dump(order)), 200

def create_order():
    data = request.get_json()
    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_order = Order(
        client_id=data['client_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        status=data['status']
    )

    db.session.add(new_order)
    db.session.commit()
    return jsonify(order_schema.dump(new_order)), 201

def get_orders_by_client(client_id):
    orders = Order.query.filter_by(client_id=client_id).all()
    return jsonify(orders_schema.dump(orders)), 200


def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()

    errors = order_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    order.client_id = data.get('client_id', order.client_id)
    order.product_id = data.get('product_id', order.product_id)
    order.quantity = data.get('quantity', order.quantity)
    order.status = data.get('status', order.status)

    db.session.commit()
    return jsonify(order_schema.dump(order)), 200

def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 204
