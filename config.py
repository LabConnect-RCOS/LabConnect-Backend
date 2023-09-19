# Import os
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))

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
