from flask import request, jsonify, Blueprint
from models.User import User
from models import db,jwt

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    print("➡️ Login request:")
    print("Email:", email)
    print("Password:", password)

    user = User.query.filter_by(email=email).first()

    if not user:
        print("❌ User not found")
        return jsonify({'error': 'Invalid email'}), 401

    if not user.check_password(password):
        print("❌ Password check failed")
        return jsonify({'error': 'Invalid password'}), 401

    
    print("✅ Login successful for:", user.email)
    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'email': user.email,
        'token': access_token  
    }), 200