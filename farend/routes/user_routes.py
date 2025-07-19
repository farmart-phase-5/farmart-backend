from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from farend.controllers.user_controllers import UserController

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    return UserController.get_users()

@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    return UserController.update_user(user_id, data)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return UserController.delete_user(user_id)