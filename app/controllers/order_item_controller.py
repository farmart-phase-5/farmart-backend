from flask import request, jsonify
from app.models.order_item import OrderItem
from app.schema.order_item_schema import order_item_schema, order_items_schema
from app import db

def create_order_item():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    order_id = data.get('order_id')
    animal_id = data.get('animal_id')
    quantity = data.get('quantity')
    price = data.get('price')
    
    new_order_item = OrderItem(
        order_id=order_id,
        animal_id=animal_id,
        quantity=quantity,
        price=price
    )
    
    db.session.add(new_order_item)
    db.session.commit()
    
    return jsonify({"message": "Order item created successfully"}), 201

def get_all_order_items():
    order_items = OrderItem.query.all()
    result = order_items_schema.dump(order_items)
    return jsonify(result), 200

def get_order_item(order_item_id):
    order_item = OrderItem.query.get(order_item_id)
    
    if not order_item:
        return jsonify({"message": "Order item not found"}), 404
    
    result = order_item_schema.dump(order_item)
    return jsonify(result), 200

def update_order_item(order_item_id):
    order_item = OrderItem.query.get(order_item_id)
    
    if not order_item:
        return jsonify({"message": "Order item not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    quantity = data.get('quantity')
    price = data.get('price')
    
    if quantity:
        order_item.quantity = quantity
    if price:
        order_item.price = price
    
    db.session.commit()
    
    return jsonify({"message": "Order item updated successfully"}), 200

def delete_order_item(order_item_id):
    order_item = OrderItem.query.get(order_item_id)
    
    if not order_item:
        return jsonify({"message": "Order item not found"}), 404
    
    db.session.delete(order_item)
    db.session.commit()
    
    return jsonify({"message": "Order item deleted successfully"}), 200

def get_order_items_by_order(order_id):
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    result = order_items_schema.dump(order_items)
    return jsonify(result), 200