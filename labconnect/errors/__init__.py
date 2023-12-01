"""
Blueprint for error pages
"""
from flask import Blueprint

error_blueprint = Blueprint("errors", __name__, template_folder="templates")

from . import routes
