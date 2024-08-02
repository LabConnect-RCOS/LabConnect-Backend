"""
Blueprint for main pages
"""

from flask import Blueprint

main_blueprint = Blueprint("main", __name__)

from . import opportunity_routes, routes, discover_routes, auth_routes
