from flask import Blueprint
from .auth_routes import auth_bp
from .user_routes import user_bp

all_routes = Blueprint('all_routes', __name__)

all_routes.register_blueprint(auth_bp)
all_routes.register_blueprint(user_bp)
