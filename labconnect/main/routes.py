from flask import render_template, Response

from . import main_blueprint


@main_blueprint.route("/")
def index():
    # return "Hello World"
    return render_template("home.html")
