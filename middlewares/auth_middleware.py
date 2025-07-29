from functools import wraps
from flask import request, jsonify, g
import jwt
from datetime import datetime
from ..models.user import User
from ..config import Config 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token missing or invalid"}), 401

        token = auth_header.split(" ")[1]

        try:
            # Decode JWT
            payload = jwt.decode(token, Config, algorithms=["HS256"])

            user_id = payload.get("user_id")
            if not user_id:
                return jsonify({"error": "Invalid token payload"}), 401

            # Fetch user from DB
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Attach user info to g
            g.user = user
            g.user_id = user.id
            g.user_role = payload.get("role")

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function
