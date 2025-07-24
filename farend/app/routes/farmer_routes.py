from flask import Blueprint, request, jsonify
from app.models import Farmer 
from app import db 


farmer_routes = Blueprint('farmer_routes', __name__)

@farmer_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if Farmer.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_farmer = Farmer(username=username, password=password)
    db.session.add(new_farmer)
    db.session.commit()

    return jsonify({"message": f"Farmer {username} registered successfully"})



@farmer_routes.route('/farmers', methods=['GET'])
def get_farmers():
    farmers = Farmer.query.all()
    return jsonify([{'id': f.id, 'username': f.username} for f in farmers])
