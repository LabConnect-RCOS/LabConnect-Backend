"""
Blueprint for main pages
"""

from flask import Blueprint

main_blueprint = Blueprint("main", __name__)

from . import auth_routes, discover_routes, opportunity_routes, routes  # noqa
