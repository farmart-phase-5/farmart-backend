from flask import jsonify, request
from ..models.user import User
from ..extensions import db
from ..config import Config
import jwt
import datetime

def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # token expires in 1 day
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def register_user(data):
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    role = data.get('role', 'customer').strip().lower()

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if role not in ['customer', 'admin']:
        return jsonify({'error': 'Invalid role specified'}), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 409

    user = User(username=username, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = generate_token(user)

    return jsonify({
        'message': 'User registered successfully',
        'role': user.role,
        'token': token
    }), 201

def login_user(data):
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = generate_token(user)

    return jsonify({
        'message': 'Login successful',
        'role': user.role,
        'token': token
    }), 200

def logout_user():
    # With JWT, logout is handled client-side by removing the token
    return jsonify({'message': 'Logged out successfully (client should discard token)'}), 200
