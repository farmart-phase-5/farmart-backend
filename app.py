from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

from farend.extensions import db, migrate
from models import jwt  
from models.User import db as legacy_db 
from controllers.auth_controller import user_bp as legacy_user_bp
from controllers.login_controller import login_bp
from farend.routes.auth_routes import auth_bp
from farend.routes.user_routes import user_bp
from farend.routes.payment_routes import payment_bp
from farend.routes.comment_routes import comment_bp

def create_app():
    app = Flask(__name__)

    
    app.config.from_object('config.Config')  
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']


  
   
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5173",
        "https://farmart-frontend-6fhz.onrender.com"
    ])

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(legacy_user_bp, url_prefix='/auth')
    app.register_blueprint(login_bp, url_prefix='/auth')

    # Import models within app context
    with app.app_context():
        from farend.models.user import User
        from farend.models.payment import Payment
        from farend.models.comments import Comments
        db.create_all()

    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to the Farmart Backend API!",
            "status": "success"
        }), 200

    # Optional: API route
    @app.route('/api')
    def api_home():
        comments = Comments.query.order_by(Comments.created_at.desc()).all()
        return jsonify({
            "message": "Welcome to Farmart API",
            "comments": [comment.serialize() for comment in comments]
        }), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)