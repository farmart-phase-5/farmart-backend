from flask import Flask
from flask_cors import CORS
from config import Config
from models.User import db
from models import jwt
from controllers.auth_controller import user_bp
from controllers.login_controller import login_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app,
     origins=["http://localhost:5173"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)
    
    db.init_app(app)
    jwt.init_app(app)
    print("For debugging purposes JWT Manager initialized")


    app.register_blueprint(user_bp, url_prefix='/auth')
    app.register_blueprint(login_bp, url_prefix='/auth')
 

    with app.app_context():
        db.create_all()

    return app