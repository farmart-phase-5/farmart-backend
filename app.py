from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    from farend.routes.auth_routes import auth_bp
    from farend.routes.user_routes import user_bp
    from farend.routes.product_routes import product_bp
    from farend.routes.order_routes import order_bp
    from farend.routes.payment_routes import payment_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(payment_bp, url_prefix='/payments')

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to Farmart API"}), 200

    return app

app = create_app()

with app.app_context():
    from farend.models.user import User
    from farend.models.products import Product
    from farend.models.order import Order
    from farend.models.payment import Payment

if __name__ == '__main__':
    app.run(debug=True)
