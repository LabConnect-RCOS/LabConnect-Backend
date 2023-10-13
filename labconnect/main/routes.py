from flask import render_template, Response

from . import main_blueprint


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/positions")
def positions():
    return render_template("positions.html")


@main_blueprint.route("/login")
def login():
    return "Login page"
    # return render_template("index.html")
