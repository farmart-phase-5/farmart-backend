from flask import jsonify
from extensions import db
from farend.models.order import Order
from farend.schema.order_schema import validate_order_data, serialize_order, serialize_orders

class OrderController:
    @staticmethod
    def create_order(data):
        validated_data, errors = validate_order_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        new_order = Order(
            user_id=validated_data['user_id'],
            product_id=validated_data['product_id'],
            quantity=validated_data['quantity'],
            total_price=validated_data['total_price'],
            status=validated_data.get('status', 'Pending')
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order created successfully", "order": serialize_order(new_order)}), 201

    @staticmethod
    def get_orders():
        orders = Order.query.all()
        return jsonify({"orders": serialize_orders(orders)}), 200

    @staticmethod
    def get_order(order_id):
        order = Order.query.get_or_404(order_id)
        return jsonify({"order": serialize_order(order)}), 200

    @staticmethod
    def update_order(order_id, data):
        order = Order.query.get_or_404(order_id)
        validated_data, errors = validate_order_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        order.user_id = validated_data.get('user_id', order.user_id)
        order.product_id = validated_data.get('product_id', order.product_id)
        order.quantity = validated_data.get('quantity', order.quantity)
        order.total_price = validated_data.get('total_price', order.total_price)
        order.status = validated_data.get('status', order.status)
        db.session.commit()
        return jsonify({"message": "Order updated successfully", "order": serialize_order(order)}), 200

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200