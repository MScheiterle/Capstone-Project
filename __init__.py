from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from routes.main.routes import main  # Handle all main routes and tasks
    # Handle all errors that the site may throw
    from routes.errors.handlers import errors
    app.register_blueprint(main)  # Register main routes to app
    app.register_blueprint(errors)  # Register error routes to app

    return app
