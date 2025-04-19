import json
import os
from datetime import datetime, timedelta, timezone
from logging.config import dictConfig

import sentry_sdk
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration

from labconnect.helpers import OrJSONProvider

# Create Database object
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app() -> Flask:
    # Create flask app object

    app = Flask(__name__)

    app.config.from_object(os.environ.get("CONFIG", "config.TestingConfig"))

    # Logging configuration
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    app.logger.info("App logger initialized.")

    # Sentry
    sentry_sdk.init(
        dsn=app.config["SENTRY_DSN"],
        integrations=[FlaskIntegration()],
        traces_sample_rate=app.config["SENTRY_TRACES_SAMPLE_RATE"],
        profiles_sample_rate=app.config["SENTRY_PROFILES_SAMPLE_RATE"],
    )

    CORS(app, supports_credentials=True, origins=[app.config["FRONTEND_URL"]])

    initialize_extensions(app)
    register_blueprints(app)

    app.logger.info("Returning App")

    return app


# ----------------
# Helper Functions
# ----------------


def initialize_extensions(app) -> None:
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    app.json = OrJSONProvider(app)

    app.logger.info("Extensions initialized.")

    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created.")

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
                    app.logger.info("Access token refreshed for user.")
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original respone
            app.logger.debug("No valid JWT found; skipping refresh.")
            return response


def register_blueprints(app) -> None:
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from labconnect.errors import error_blueprint
    from labconnect.main import main_blueprint

    app.register_blueprint(main_blueprint)
    app.logger.info("Main blueprint registered.")

    app.register_blueprint(error_blueprint)
    app.logger.info("Error blueprint registered.")
