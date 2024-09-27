import json
import os

from datetime import datetime, timedelta, timezone

# Import Flask modules
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
)

from flask_sqlalchemy import SQLAlchemy

import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration

from labconnect.helpers import OrJSONProvider

# Create Database object
db = SQLAlchemy()
jwt = JWTManager()


def create_app() -> Flask:
    # Create flask app object
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(os.environ.get("CONFIG", "config.TestingConfig"))

    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration()],
        traces_sample_rate=app.config['SENTRY_TRACES_SAMPLE_RATE'],
        profiles_sample_rate=app.config['SENTRY_PROFILES_SAMPLE_RATE'],

    )

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
    jwt.init_app(app)
    app.json = OrJSONProvider(app)

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
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original respone
            return response


def register_blueprints(app) -> None:
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from labconnect.errors import error_blueprint
    from labconnect.main import main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(error_blueprint)
