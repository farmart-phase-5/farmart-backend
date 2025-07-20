from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from farend.controllers.user_controllers import UserController

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    return UserController.create_user(data)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    return UserController.get_users()

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    return UserController.get_user(user_id)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    return UserController.update_user(user_id, data)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return UserController.delete_user(user_id)