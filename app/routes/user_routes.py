from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200
