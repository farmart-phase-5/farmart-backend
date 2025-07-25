from flask import request, jsonify
from app.models.order_model import Order
from app.schema.order_schema import order_schema, orders_schema
from app import db
from datetime import datetime

def create_order():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    animal_id = data.get('animal_id')
    quantity = data.get('quantity')
    total_price = data.get('total_price')
    status = data.get('status', 'pending')
    
    new_order = Order(
        animal_id=animal_id,
        quantity=quantity,
        total_price=total_price,
        status=status,
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({"message": "Order created successfully"}), 201

def get_all_orders():
    orders = Order.query.all()
    result = orders_schema.dump(orders)
    return jsonify(result), 200

def get_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    result = order_schema.dump(order)
    return jsonify(result), 200

def update_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    quantity = data.get('quantity')
    total_price = data.get('total_price')
    status = data.get('status')
    
    if quantity:
        order.quantity = quantity
    if total_price:
        order.total_price = total_price
    if status:
        order.status = status
    
    db.session.commit()
    
    return jsonify({"message": "Order updated successfully"}), 200

def delete_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({"message": "Order deleted successfully"}), 200

def get_animal_orders(animal_id):
    orders = Order.query.filter_by(animal_id=animal_id).all()
    result = orders_schema.dump(orders)
    return jsonify(result), 200