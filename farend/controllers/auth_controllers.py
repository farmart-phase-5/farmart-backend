from flask import Blueprint, request, jsonify
from farend.models.user import User
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'client')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401
