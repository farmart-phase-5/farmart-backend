from flask import jsonify
from extensions import db
from farend.models.user import User
from farend.schema.user_schema import validate_user_data, serialize_user, serialize_users

class UserController:
    @staticmethod
    def create_user(data):
        validated_data, errors = validate_user_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        new_user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'client')
        )
        new_user.set_password(validated_data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user": serialize_user(new_user)}), 201

    @staticmethod
    def get_users():
        users = User.query.all()
        return jsonify({"users": serialize_users(users)}), 200

    @staticmethod
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({"user": serialize_user(user)}), 200

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get_or_404(user_id)
        validated_data, errors = validate_user_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.role = validated_data.get('role', user.role)
        db.session.commit()
        return jsonify({"message": "User updated successfully", "user": serialize_user(user)}), 200

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200