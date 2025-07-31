def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.json.compact = False

    db.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    return app
