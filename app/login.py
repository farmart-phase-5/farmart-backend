from flask import Blueprint, request, jsonify
from app.models.user import User
from app.user_schema import RegisterSchema, LoginSchema
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    errors = RegisterSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409
    user = user(
         username=data['username'],
        email=data['email'],
        role=data['role']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({
        "access_token": token,
        "user": user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful."}), 200
