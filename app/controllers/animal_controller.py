from flask import request, jsonify
from app.models.animal_model import Animal
from app.schema.animal_schema import animal_schema, animals_schema
from app import db

def create_animal():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    name = data.get('name')
    species = data.get('species')
    breed = data.get('breed')
    age = data.get('age')
    farmer_id = data.get('farmer_id')
    
    new_animal = Animal(
        name=name,
        species=species,
        breed=breed,
        age=age,
        farmer_id=farmer_id
    )
    
    db.session.add(new_animal)
    db.session.commit()
    
    return jsonify({"message": "Animal created successfully"}), 201

def get_all_animals():
    animals = Animal.query.all()
    result = animals_schema.dump(animals)
    return jsonify(result), 200

def get_animal(animal_id):
    animal = Animal.query.get(animal_id)
    
    if not animal:
        return jsonify({"message": "Animal not found"}), 404
    
    result = animal_schema.dump(animal)
    return jsonify(result), 200

def update_animal(animal_id):
    animal = Animal.query.get(animal_id)
    
    if not animal:
        return jsonify({"message": "Animal not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    name = data.get('name')
    species = data.get('species')
    breed = data.get('breed')
    age = data.get('age')
    
    if name:
        animal.name = name
    if species:
        animal.species = species
    if breed:
        animal.breed = breed
    if age:
        animal.age = age
    
    db.session.commit()
    
    return jsonify({"message": "Animal updated successfully"}), 200

def delete_animal(animal_id):
    animal = Animal.query.get(animal_id)
    
    if not animal:
        return jsonify({"message": "Animal not found"}), 404
    
    db.session.delete(animal)
    db.session.commit()
    
    return jsonify({"message": "Animal deleted successfully"}), 200

def get_farmer_animals(farmer_id):
    animals = Animal.query.filter_by(farmer_id=farmer_id).all()
    result = animals_schema.dump(animals)
    return jsonify(result), 200