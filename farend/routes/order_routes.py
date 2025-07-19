from flask import Blueprint, request, jsonify
from extensions import db
from farend.models.order import Order
from farend.models.user import User
from farend.models.products import Product

order_bp = Blueprint('orders', __name__)

@order_bp.route('/checkout', methods=['POST'])
def create_checkout():
    data = request.get_json()

    client_id = data.get('client_id')
    product_ids = data.get('product_ids')

    if not client_id or not isinstance(product_ids, list):
        return jsonify({"error": "Invalid input. client_id and product_ids required."}), 400

    user = User.query.get(client_id)
    if not user:
        return jsonify({"error": "Client not found."}), 404

    orders = []
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": f"Product with id {product_id} not found."}), 404

        order = Order(client_id=client_id, product_id=product_id)
        db.session.add(order)
        orders.append(order)

    db.session.commit()

    return jsonify({"message": "Order created successfully.", "orders": [o.serialize() for o in orders]}), 201

@order_bp.route('/checkout/<int:client_id>', methods=['DELETE'])
def delete_checkout(client_id):
    orders = Order.query.filter_by(client_id=client_id).all()
    if not orders:
        return jsonify({"error": "No orders found for this client."}), 404

    for order in orders:
        db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "All orders for the client have been deleted."}), 200

@order_bp.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    data = request.get_json()

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found."}), 404

    new_product_id = data.get('product_id')
    if new_product_id:
        product = Product.query.get(new_product_id)
        if not product:
            return jsonify({"error": "New product not found."}), 404
        order.product_id = new_product_id

    db.session.commit()
    return jsonify({"message": "Order updated successfully.", "order": order.serialize()}), 200

@order_bp.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found."}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted successfully."}), 200
