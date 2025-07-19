from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db, ma, jwt
from farend.routes.auth_routes import auth_bp
from farend.routes.order_routes import order_bp
from farend.routes.product_routes import product_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key' 

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(product_bp, url_prefix='/api/products')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
