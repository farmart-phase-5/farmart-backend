from flask import request, jsonify
from farend.models.user import User
from farend.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class AuthController:

    @staticmethod
    def register():
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return jsonify({"error": "Username and password required"}), 400

        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already exists"}), 400

        hashed_password = generate_password_hash(data["password"])
        user = User(username=data["username"], password_hash=hashed_password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "user": user.username}), 201

    @staticmethod
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data.get("username")).first()

        if user and check_password_hash(user.password_hash, data.get("password")):
            return jsonify({"message": "Login successful", "user": user.username}), 200

        return jsonify({"error": "Invalid credentials"}), 401
