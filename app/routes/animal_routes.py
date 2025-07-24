from flask import Blueprint, request, jsonify
from app import db
from app.models.animal_model import Animal

animal_routes = Blueprint('animal_routes', __name__)


@animal_routes.route('/', methods=['POST'])
def create_animal():  
    data = request.get_json()
    try:
        animal = Animal(
            name=data['name'],
            breed=data['breed'],
            age=data['age'],
            price=data['price'],
            farmer_id=data['farmer_id']
        )
        db.session.add(animal)
        db.session.commit()
        return jsonify(animal.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@animal_routes.route('/', methods=['GET'])
def get_animals():
    animal_type = request.args.get('type')
    min_price = request.args.get('min_price', type=float)
    query = Animal.query
    if animal_type:
        query = query.filter(Animal.breed == animal_type)
    if min_price is not None:
        query = query.filter(Animal.price >= min_price)
    animals = query.all()
    return jsonify([animal.to_dict() for animal in animals]), 200

@animal_routes.route('/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get_or_404(id)
    return jsonify(animal.to_dict()), 200


@animal_routes.route('/farmers/<int:farmer_id>/animals', methods=['GET'])
def get_animals_by_farmer(farmer_id):
    animals = Animal.query.filter_by(farmer_id=farmer_id).all()
    return jsonify([animal.to_dict() for animal in animals]), 200


@animal_routes.route('/<int:id>', methods=['PATCH'])
def update_animal(id):
    animal = Animal.query.get_or_404(id)
    data = request.get_json()
    for field in ['name', 'breed', 'age', 'price', 'farmer_id']:
        if field in data:
            setattr(animal, field, data[field])
    db.session.commit()
    return jsonify(animal.to_dict()), 200

#
@animal_routes.route('/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': 'Animal deleted successfully'}), 200
