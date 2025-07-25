from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/farmart.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secure-jwt-secret-key-here')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secure-secret-key-here')
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5173",
        "https://farmart-frontend-6fhz.onrender.com"
    ])
    
    from farend.routes.auth_routes import auth_bp
    from farend.routes.user_routes import user_bp
    from farend.routes.payment_routes import payment_bp
    from farend.routes.comment_routes import comment_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(comment_bp)
    
    try:
        from farend.routes.product_routes import product_bp
        app.register_blueprint(product_bp)
    except ImportError:
        print("Warning: Could not import product_bp from farend.routes.product_routes")
    
    try:
        from farend.routes.order_route import order_bp as farend_order_bp
        app.register_blueprint(farend_order_bp)
    except ImportError:
        print("Warning: Could not import order_bp from farend.routes.order_route")
    
    with app.app_context():

        from farend.models.user import User
        from farend.models.payment import Payment
        from farend.models.comments import Comments
        
        try:
            from farend.models.products import Product
        except ImportError:
            print("Warning: Could not import Product from farend.models.products")
        
        try:
            from farend.models.order import Order as FarendOrder
        except ImportError:
            print("Warning: Could not import Order from farend.models.order")
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to the Farmart Backend API!",
            "status": "success"
        }), 200
    
    @app.route('/api')
    def api_home():
        return jsonify({
            "message": "Welcome to Farmart API"
        }), 200
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
