from flask import request, jsonify
from farend.models.user import User
from extensions import db
from farend.schema.user_schema import user_schema, users_schema


class UserController:

    @staticmethod
    def get_users():
        users = User.query.all()
        return jsonify(users_schema.dump(users)), 200

    @staticmethod
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user_schema.dump(user)), 200

    @staticmethod
    def create_user():
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return jsonify(errors), 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'client')
        )
        new_user.set_password(data.get('password', 'defaultpass'))

        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201

    @staticmethod
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        errors = user_schema.validate(data, partial=True)
        if errors:
            return jsonify(errors), 400

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)

        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()
        return jsonify(user_schema.dump(user)), 200

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 204
