import logging
import os

# Import Flask modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf_protection = CSRFProtect()

# Create Database object
db = SQLAlchemy()


def create_app() -> Flask:
    # Create flask app object
    app = Flask(__name__)
    app.config.from_object(os.environ.get("CONFIG", "config.TestingConfig"))

    initialize_extensions(app)
    register_blueprints(app)

    return app


# ----------------
# Helper Functions
# ----------------


def initialize_extensions(app) -> None:
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    csrf_protection.init_app(app)

    # Flask-Login configuration
    from labconnect.models import RPIDepartments

    # @login.user_loader
    # def load_user(user_id):
    #     return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app) -> None:
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from labconnect.errors import error_blueprint
    from labconnect.main import main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(error_blueprint)
