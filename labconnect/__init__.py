import os

# Import Flask modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

environment = os.environ.get("CONFIG", "config.TestingConfig")

# Create flask app object
app = Flask(__name__)
app.config.from_object(environment)

# Create Database object
# db = SQLAlchemy(app)

# Import all views
import labconnect.views
