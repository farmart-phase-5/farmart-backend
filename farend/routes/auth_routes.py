from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from farend.extensions import db
from farend.models.user import User
from farend.schema.user_schema import validate_user_data, serialize_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validated_data, errors = validate_user_data(data)
    if errors:
        return jsonify({"error": errors}), 400

    new_user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        role=validated_data.get('farmer', 'client')
    )
    new_user.set_password(validated_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": serialize_user(new_user)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' and 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity = user.id)
        return jsonify({"message": "Login successful", "access_token": access_token, "user": serialize_user(user)}), 200
    return jsonify({"error": "Invalid credentials"}), 401