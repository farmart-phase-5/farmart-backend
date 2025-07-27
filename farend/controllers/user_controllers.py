from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db

user_bp = Blueprint('users', __name__)
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
