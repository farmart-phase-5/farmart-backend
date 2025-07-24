from flask import Blueprint, request, jsonify
from app import db
from app.models import Farmer

farmer_routes = Blueprint('farmer_routes', __name__)

# Register a new farmer
@farmer_routes.route('/register', methods=['POST'])
def register_farmer():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    location = data.get('location')
    contact = data.get('contact')
    note = data.get('note')

    if Farmer.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    new_farmer = Farmer(
        name=name,
        username=username,
        password=password,
        location=location,
        contact=contact,
        note=note
    )
    db.session.add(new_farmer)
    db.session.commit()

    return jsonify({'message': 'Farmer created successfully'}), 201

# Get all farmers
@farmer_routes.route('/', methods=['GET'])
def get_farmers():
    farmers = Farmer.query.all()
    result = [{
        'id': f.id,
        'name': f.name,
        'username': f.username,
        'location': f.location,
        'contact': f.contact,
        'note': f.note
    } for f in farmers]
    return jsonify(result)

# Get a specific farmer by ID
@farmer_routes.route('/<int:id>', methods=['GET'])
def get_farmer(id):
    farmer = Farmer.query.get(id)
    if not farmer:
        return jsonify({'error': 'Farmer not found'}), 404

    return jsonify({
        'id': farmer.id,
        'name': farmer.name,
        'username': farmer.username,
        'location': farmer.location,
        'contact': farmer.contact,
        'note': farmer.note
    })

# Update a farmer
@farmer_routes.route('/<int:id>', methods=['PATCH'])
def update_farmer(id):
    farmer = Farmer.query.get(id)
    if not farmer:
        return jsonify({'error': 'Farmer not found'}), 404

    data = request.get_json()
    farmer.name = data.get('name', farmer.name)
    farmer.username = data.get('username', farmer.username)
    farmer.password = data.get('password', farmer.password)
    farmer.location = data.get('location', farmer.location)
    farmer.contact = data.get('contact', farmer.contact)
    farmer.note = data.get('note', farmer.note)

    db.session.commit()
    return jsonify({'message': 'Farmer updated successfully'})

# Delete a farmer
@farmer_routes.route('/<int:id>', methods=['DELETE'])
def delete_farmer(id):
    farmer = Farmer.query.get(id)
    if not farmer:
        return jsonify({'error': 'Farmer not found'}), 404

    try:
        db.session.delete(farmer)
        db.session.commit()
        return jsonify({'message': 'Farmer deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500