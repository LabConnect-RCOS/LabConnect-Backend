# Import os
from os import getenv, path
from datetime import timedelta

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))


class Config:
    load_dotenv()

    # Configuration
    SECRET_KEY = getenv("SECRET_KEY", "main-secret")

    TESTING = False
    DEBUG = False

    PREFERRED_URL_SCHEME = "https"

    SAML_CONFIG = path.join(basedir, "config/saml/")
    FRONTEND_URL = getenv("FRONTEND_URL", "http://localhost:3000")

    SENTRY_DSN = getenv("SENTRY_DSN", "")
    SENTRY_TRACES_SAMPLE_RATE = float(getenv("SENTRY_TRACES_SAMPLE_RATE", 1.0))
    SENTRY_PROFILES_SAMPLE_RATE = float(getenv("SENTRY_PROFILES_SAMPLE_RATE", 1.0))

    SQLALCHEMY_DATABASE_URI = getenv(
        "DB", "postgresql+psycopg2://postgres:root@localhost/labconnect"
    )

    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_SESSION_COOKIE = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = "Strict"
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    JWT_COOKIE_SECURE = False


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
