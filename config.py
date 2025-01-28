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
    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

    SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
    SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", 1.0))
    SENTRY_PROFILES_SAMPLE_RATE = float(
        os.environ.get("SENTRY_PROFILES_SAMPLE_RATE", 1.0)
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DB", "postgresql+psycopg2://postgres:root@localhost/labconnect"
    )

    TOKEN_BLACKLIST = set()


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
