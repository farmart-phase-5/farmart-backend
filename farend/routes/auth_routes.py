from flask import Blueprint, request, jsonify
from farend.controllers.auth_controllers import AuthController
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return AuthController.register(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return AuthController.login(data)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    return AuthController.get_profile(user_id)