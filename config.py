# Import os
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(32))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    TESTING = False
    DEBUG = False

    PREFERRED_URL_SCHEME = "https"

    SAML_CONFIG = os.path.join(basedir, "config/saml/")
    FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://labconnect.cs.rpi.edu")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    # Using SQLLITE locally
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'database.db')}"


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False

    # Using SQLLITE locally as a fallback, the goal is to use postgresql in production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DB", f"sqlite:///{os.path.join(basedir, 'db', 'database.db')}"
    )
