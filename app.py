from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys, os
sys.path.append(os.path.dirname(__file__))
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from extension import db, jwt
from models.farmer import Farmer
from models.animals import Animals


 

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from controllers.animals_controller import animals_bp
    from controllers.cart_controller import cart_bp

    app.register_blueprint(animals_bp, url_prefix='/animals')
    app.register_blueprint(cart_bp, url_prefix='/cart')

    return app
