from flask import Flask
from flask_migrate import Migrate
from .config import Config, Auth_config
from .main.routes import main    
from .main.models import db
from .modify.routes import modify
from .auth.auth import oauth
from .auth.routes import auth
from .errors.handlers import errors


migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = Auth_config.AUTH0_CLIENT_SECRET
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(modify)
    app.register_blueprint(errors)

    return app