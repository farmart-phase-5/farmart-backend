from flask import Flask
from extensions import db, jwt, migrate, bcrypt
from routes import routes_bp
from config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(routes_bp)

    @app.route('/')
    def index():
        return {'message': 'Farmart API is running successfully!'}

    return app
