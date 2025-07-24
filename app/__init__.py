from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import models
    from app.models import farmer_model, animal_model, order_model

    # Import Blueprints
    from app.routes.farmer_routes import farmer_routes
    from app.routes.animal_routes import animal_routes
    from app.routes.order_routes import order_routes

    # Register Blueprints with prefixes
    app.register_blueprint(farmer_routes, url_prefix='/farmers')
    app.register_blueprint(animal_routes, url_prefix='/animals')
    app.register_blueprint(order_routes, url_prefix='/orders')

    # Root route
    @app.route('/')
    def home():
        return "Welcome to my Farmart server"

    # Debug print
    print("Registered Routes:")
    print(app.url_map)

    app.debug = True
    return app
