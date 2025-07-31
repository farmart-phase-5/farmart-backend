from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, 
    get_jwt_identity, get_jwt
)
from flask_restful import Api
from datetime import datetime, timedelta
from functools import wraps
import os
from flask_cors import CORS
from config import db
from models import User, Animal, CartItem, Order, OrderItem
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)


CORS(app,
     origins=[
         "http://localhost:5173",
         "https://farmart-frontend-6fhz.onrender.com"
     ],
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])


blacklist = set()
serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'admin':
            return jsonify({
                'error': 'Admin privileges required',
                'status': 403
            }), 403
        return f(*args, **kwargs)
    return decorated

def farmer_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role not in ['admin', 'farmer']:
            return jsonify({
                'error': 'Farmer privileges required',
                'status': 403
            }), 403
        return f(*args, **kwargs)
    return decorated


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token has been revoked',
        'status': 401
    }), 401


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad request',
        'message': str(error),
        'status': 400
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': str(error),
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': str(error),
        'status': 500
    }), 500


@app.route('/healthcheck')
def healthcheck():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

# Auth routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
    
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'error': 'Email already exists'
        }), 409
    
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
    
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Registration successful',
            'access_token': access_token,
            'token': access_token,
            'user': user.to_dict(),
            'expires_in': app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user.id)

        response = jsonify({
            "access_token": access_token,
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role
            },
            "expires_in": 3600
        })
        
        response.set_cookie(
            'access_token_cookie',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=3600
        )
        
        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({
        'message': 'Successfully logged out'
    }), 200

@app.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    return jsonify(user.to_dict()), 200


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    
    if 'email' not in data:
        return jsonify({
            'error': 'Email is required'
        }), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({
            'error': 'No account with that email exists'
        }), 404
    
    token = serializer.dumps(user.email, salt='password-reset')
    reset_url = f"https://farmart-frontend-6fhz.onrender.com/reset-password/{token}"
    
    return jsonify({
        'message': 'Password reset link generated',
        'reset_url': reset_url 
    }), 200

@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    
    if 'password' not in data:
        return jsonify({
            'error': 'Password is required'
        }), 400
    
    try:
        email = serializer.loads(
            token,
            salt='password-reset',
            max_age=3600  
        )
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                'error': 'User not found'
            }), 404
            
        user.set_password(data['password'])
        db.session.commit()
        
        return jsonify({
            'message': 'Password successfully reset'
        }), 200
        
    except SignatureExpired:
        return jsonify({
            'error': 'Reset token has expired'
        }), 400
    except BadSignature:
        return jsonify({
            'error': 'Invalid reset token'
        }), 400


@app.route('/animals', methods=['GET'])
def get_animals():
    animals = Animal.query.all()
    return jsonify([a.to_dict() for a in animals]), 200

@app.route('/animals/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return jsonify(animal.to_dict()), 200

@app.route('/animals', methods=['POST'])
@jwt_required()
def create_animal():
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        animal = Animal(
            name=data['name'],
            type=data['type'],
            breed=data['breed'],
            price=data['price'],
            image=data.get('image', ''),
            farmer_id=user_id
        )
        db.session.add(animal)
        db.session.commit()
        return jsonify(animal.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/animals/<int:animal_id>', methods=['PATCH'])
@jwt_required()
def update_animal(animal_id):
    user_id = get_jwt_identity()
    animal = Animal.query.get_or_404(animal_id)
    if animal.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    for key in data:
        setattr(animal, key, data[key])
    db.session.commit()
    return jsonify(animal.to_dict()), 200

@app.route('/animals/<int:animal_id>', methods=['DELETE'])
@jwt_required()
def delete_animal(animal_id):
    user_id = get_jwt_identity()
    animal = Animal.query.get_or_404(animal_id)
    if animal.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': 'Animal deleted'}), 200

# ---------------- CART ROUTES ---------------- #
@app.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in cart_items]), 200

@app.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    item = CartItem(
        user_id=user_id,
        animal_id=data['animal_id'],
        quantity=data.get('quantity', 1)
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(item_id):
    user_id = get_jwt_identity()
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from cart'}), 200

@app.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    total = sum(item.animal.price * item.quantity for item in cart_items)
    order = Order(user_id=user_id, total_price=total)
    db.session.add(order)
    db.session.flush()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            animal_id=item.animal_id,
            quantity=item.quantity
        )
        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()
    return jsonify(order.to_dict()), 201

# ---------------- ORDERS ---------------- #
@app.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([o.to_dict() for o in orders]), 200 

@app.route('/orders/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_order_status(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    user = User.query.get(user_id)

    if user.role != 'farmer':
        return jsonify({'error': 'Only farmers can confirm/reject orders'}), 403

    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify(order.to_dict()), 200

# ---------------- ADMIN ---------------- #
@app.route('/admin/orders', methods=['GET'])
@admin_required
def get_all_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders]), 200

@app.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@app.route('/admin/animals', methods=['GET'])
@admin_required
def get_all_animals_admin():
    animals = Animal.query.all()
    return jsonify([a.to_dict() for a in animals]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5555)))
