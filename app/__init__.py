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

    from app.models import Farmer, Animal, Order, OrderItem, Cart, CartItem

    
    from app.routes.farmer_routes import farmer_routes
    from app.routes.animal_routes import animal_routes
    from app.routes.order_routes import order_routes
    from app.routes.cart_routes import cart_routes
    from app.routes.cart_item_routes import cart_item_routes  


    app.register_blueprint(farmer_routes, url_prefix='/farmers')
    app.register_blueprint(animal_routes, url_prefix='/animals')
    app.register_blueprint(order_routes, url_prefix='/orders')
    app.register_blueprint(cart_routes)  
    app.register_blueprint(cart_item_routes)  

    @app.route('/')
    def home():
        return " Welcome to the Farmart Server"

    if app.config['DEBUG']:
        print("📋 Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.methods} → {rule}")

    return app
