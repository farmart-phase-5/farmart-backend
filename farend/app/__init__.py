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

    from .models.farmer_model import Farmer
    from .models.animal_model import Animal
    from .models.order_model import Order

    
    @app.route('/')
    def home():
        return "Welcome to my Farmart server"


    from .routes.farmer_routes import farmer_routes
    app.register_blueprint(farmer_routes, url_prefix='/farmer')

    from .routes.order_routes import order_routes
    app.register_blueprint(order_routes)

    from .routes.animal_routes import animal_routes
    app.register_blueprint(animal_routes)

  
    # app.debug = True

    return app
