from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .main.routes import main    
from .main.models import db
from .errors.handlers import errors

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app