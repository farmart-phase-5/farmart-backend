from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import db, User
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Register route
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already in use"}), 400

    try:
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password']) 

        db.session.add(new_user)
        db.session.commit()
        print("Creating user:", data)
        print("Password (raw):", data['password'])
        print("Password (hashed):", new_user.password_hash)
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    