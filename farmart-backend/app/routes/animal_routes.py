from flask import Blueprint, request, jsonify
from app.models import Animal
from app import db

animal_routes = Blueprint('animal_routes', __name__)


@animal_routes.route('/animals', methods=['POST'])
def create_animal():
    data = request.get_json()

    name = data.get('name')
    type_ = data.get('type')
    breed = data.get('breed')
    age = data.get('age')
    price = data.get('price')
    farmer_id = data.get('farmer_id')

    if not name or not type_ or not farmer_id:
        return jsonify({'error': 'Name, type, and farmer_id are required'}), 400

    new_animal = Animal(
        name=name,
        type=type_,
        breed=breed,
        age=age,
        price=price,
        farmer_id=farmer_id
    )
    db.session.add(new_animal)
    db.session.commit()

    return jsonify({
        'id': new_animal.id,
        'name': new_animal.name,
        'type': new_animal.type,
        'breed': new_animal.breed,
        'age': new_animal.age,
        'price': new_animal.price,
        'farmer_id': new_animal.farmer_id
    }), 201

@animal_routes.route('/animals', methods=['GET'])
def get_animals():
    animals = Animal.query.all()
    animal_list = [{
        'id': animal.id,
        'name': animal.name,
        'type': animal.type,
        'breed': animal.breed,
        'age': animal.age,
        'price': animal.price,
        'farmer_id': animal.farmer_id
    } for animal in animals]

    return jsonify(animal_list), 200

@animal_routes.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error': f'Animal with ID {id} not found.'}), 404

    return jsonify({
        'id': animal.id,
        'name': animal.name,
        'type': animal.type,
        'breed': animal.breed,
        'age': animal.age,
        'price': animal.price,
        'farmer_id': animal.farmer_id
    }), 200


@animal_routes.route('/animals/<int:id>', methods=['PATCH'])
def update_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404

    data = request.get_json()

    if 'name' in data:
        animal.name = data['name']
    if 'type' in data:
        animal.type = data['type']
    if 'breed' in data:
        animal.breed = data['breed']
    if 'age' in data:
        animal.age = data['age']
    if 'price' in data:
        animal.price = data['price']
    if 'farmer_id' in data:
        animal.farmer_id = data['farmer_id']

    db.session.commit()

    return jsonify({
        'id': animal.id,
        'name': animal.name,
        'type': animal.type,
        'breed': animal.breed,
        'age': animal.age,
        'price': animal.price,
        'farmer_id': animal.farmer_id
    }), 200


@animal_routes.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': f'Animal with ID {id} has been deleted.'}), 200
