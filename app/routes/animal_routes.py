from flask import Blueprint, request, jsonify
from app import db
from app.models.animal_model import Animal
from sqlalchemy.exc import SQLAlchemyError

animal_routes = Blueprint('animal_routes', __name__)

@animal_routes.route('/', methods=['POST'])
def create_animal():
    data = request.get_json()
    
  
    required_fields = ['name', 'breed', 'price', 'farmer_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
       
        if Animal.query.filter_by(name=data['name'], farmer_id=data['farmer_id']).first():
            return jsonify({'error': 'Animal already exists for this farmer'}), 409
            
        animal = Animal(
            name=data['name'],
            breed=data['breed'],
            age=data.get('age'), 
            price=float(data['price']),  
            farmer_id=data['farmer_id']
        )
        
        db.session.add(animal)
        db.session.commit()
        return jsonify(animal.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

@animal_routes.route('/', methods=['GET'])
def get_animals():
    try:
        animal_type = request.args.get('type')
        min_price = request.args.get('min_price', type=float)
        
        query = Animal.query
        
        if animal_type:
            query = query.filter(Animal.breed.ilike(f'%{animal_type}%')) 
            
        if min_price is not None:
            query = query.filter(Animal.price >= min_price)
            
        animals = query.all()
        return jsonify([animal.to_dict() for animal in animals]), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

@animal_routes.route('/<int:id>', methods=['GET'])
def get_animal(id):
    try:
        animal = Animal.query.get_or_404(id)
        return jsonify(animal.to_dict()), 200
    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500

@animal_routes.route('/farmers/<int:farmer_id>/animals', methods=['GET'])
def get_animals_by_farmer(farmer_id):
    try:
        animals = Animal.query.filter_by(farmer_id=farmer_id).all()
        if not animals:
            return jsonify({'message': 'No animals found for this farmer'}), 200
        return jsonify([animal.to_dict() for animal in animals]), 200
    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500

@animal_routes.route('/<int:id>', methods=['PATCH'])
def update_animal(id):
    try:
        animal = Animal.query.get_or_404(id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        updatable_fields = ['name', 'breed', 'age', 'price']
        for field in updatable_fields:
            if field in data:
                if field == 'price':
                    setattr(animal, field, float(data[field]))  
                else:
                    setattr(animal, field, data[field])
                    
        db.session.commit()
        return jsonify(animal.to_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

@animal_routes.route('/<int:id>', methods=['DELETE'])
def delete_animal(id):
    try:
        animal = Animal.query.get_or_404(id)
        db.session.delete(animal)
        db.session.commit()
        return jsonify({'message': 'Animal deleted successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500