from flask import jsonify, session
from ..models.user import User
from ..extensions import db

def register_user(data):
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    role = data.get('role', 'customer').strip().lower()

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if role not in ['customer', 'admin']:  # adjust roles as needed
        return jsonify({'error': 'Invalid role specified'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    user = User(username=username, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'role': user.role}), 201

def login_user(data):
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = user.id
    session['role'] = user.role

    return jsonify({'message': 'Login successful', 'role': user.role}), 200

def logout_user():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
