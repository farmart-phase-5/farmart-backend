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
    from . import models  # Register models
    migrate.init_app(app, db)
    CORS(app)

    # ✅ Add the homepage route here
    @app.route('/')
    def home():
        return "Hello, Farmart!"

    from .routes.farmer_routes import farmer_routes
    app.register_blueprint(farmer_routes, url_prefix='/farmer')

    # Import and register the order routes blueprint
    from .routes.order_routes import order_routes
    app.register_blueprint(order_routes)

    return app
