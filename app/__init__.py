from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    with app.app_context():
        from .models.farmer_model import Farmer
        from .models.animal_model import Animal
        from .models.order_model import Order
        from .models.order_item import OrderItem
    
    @app.route('/')
    def home():
        return "Welcome to my Farmart server"
    
    # Register blueprints
    from .routes.farmer_routes import farmer_routes
    app.register_blueprint(farmer_routes, url_prefix='/api/farmer')
    
    from .routes.order_routes import order_routes
    app.register_blueprint(order_routes, url_prefix='/api/order')
    
    from .routes.animal_routes import animal_routes
    app.register_blueprint(animal_routes, url_prefix='/api/animal')
    
    from .routes.order_item_routes import order_item_routes
    app.register_blueprint(order_item_routes)
    
    return app
