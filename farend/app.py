from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

from farend.routes.auth_routes import auth_bp
from farend.routes.user_routes import user_bp
from farend.routes.payment_routes import payment_bp
from farend.routes.comment_routes import comment_bp

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(comment_bp)

    with app.app_context():
        from farend.models.user import User
        from farend.models.products import Product
        from farend.models.order import Order
        from farend.models.payment import Payment
        from farend.models.comments import Comment

        @app.route('/')
        def index():
            comments = Comment.query.order_by(Comment.created_at.desc()).all()
            return jsonify({
                "message": "Welcome to Farmart API",
                "comments": [comment.serialize() for comment in comments]
            }), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
