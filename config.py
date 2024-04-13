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


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    # Using SQLLITE locally
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'database.db')}"


class ProductionConfig(Config):
    pass
