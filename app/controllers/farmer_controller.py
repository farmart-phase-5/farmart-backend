from flask import request, jsonify
from app.models.farmer_model import Farmer
from app.schema.farmer_schema import farmer_schema, farmers_schema
from app import db

def register_farmer():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if Farmer.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    
    new_farmer = Farmer(username=username, password=password)
    
    db.session.add(new_farmer)
    db.session.commit()
    
    return jsonify({"message": f"Farmer {username} registered successfully"}), 201

def get_all_farmers():
    farmers = Farmer.query.all()
    result = farmers_schema.dump(farmers)
    return jsonify(result), 200

def get_farmer(farmer_id):
    farmer = Farmer.query.get(farmer_id)
    
    if not farmer:
        return jsonify({"message": "Farmer not found"}), 404
    
    result = farmer_schema.dump(farmer)
    return jsonify(result), 200

def update_farmer(farmer_id):
    farmer = Farmer.query.get(farmer_id)
    
    if not farmer:
        return jsonify({"message": "Farmer not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    username = data.get('username')
    
    if username:
        existing_farmer = Farmer.query.filter_by(username=username).first()
        if existing_farmer and existing_farmer.id != farmer_id:
            return jsonify({"message": "Username already exists"}), 400
        farmer.username = username
    
    db.session.commit()
    
    return jsonify({"message": "Farmer updated successfully"}), 200

def delete_farmer(farmer_id):
    farmer = Farmer.query.get(farmer_id)
    
    if not farmer:
        return jsonify({"message": "Farmer not found"}), 404
    
    db.session.delete(farmer)
    db.session.commit()
    
    return jsonify({"message": "Farmer deleted successfully"}), 200