from flask import Blueprint, jsonify, request, abort
from models.animals import Animals
from schemas.animal_schema import AnimalSchema
from farend.extensions import db


animals_bp = Blueprint('animals', __name__)
animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)


@animals_bp.route('/', methods=['GET'])
def get_animals():
    query = Animals.query

    type_filter = request.args.get('type')
    breed_filter = request.args.get('breed')
    age_filter = request.args.get('age')

    if type_filter:
        query = query.filter_by(type=type_filter)
    if breed_filter:
        query = query.filter_by(breed=breed_filter)
    if age_filter:
        query = query.filter_by(age=int(age_filter))

    animals = query.all()
    return jsonify(animals_schema.dump(animals))


@animals_bp.route('/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animals.query.get_or_404(id)
    return jsonify(animal_schema.dump(animal))


@animals_bp.route('/', methods=['POST'])
def create_animal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

  
    try:
        new_animal = animal_schema.load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    db.session.add(new_animal)
    db.session.commit()
    return jsonify(animal_schema.dump(new_animal)), 201


@animals_bp.route('/<int:id>', methods=['PATCH'])
def update_animal(id):
    animal = Animals.query.get_or_404(id)
    data = request.get_json()

    
    for key, value in data.items():
        if hasattr(animal, key):
            setattr(animal, key, value)

    db.session.commit()
    return jsonify(animal_schema.dump(animal))


@animals_bp.route('/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animals.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": f"Animal {id} deleted successfully"}), 200

