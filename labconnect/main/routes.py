from flask import render_template, Response

from . import main_blueprint


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/positions")
def positions():
    return render_template("positions.html")


@main_blueprint.route("/profile/<str:rcs_id>")
def profile(rcs_id: str):
    return render_template("profile.html")


@main_blueprint.route("/department")
def department():
    return render_template("department.html")


@main_blueprint.route("/discover")
def discover():
    return render_template("discover.html")


@main_blueprint.route("/professor/<str:rcs_id>")
def professor(rcs_id: str):
    return render_template("professor.html")


@main_blueprint.route("/create_post")
def create_post():
    return render_template("posting.html")


@main_blueprint.route("/login")
def login():
    return "Login page"
    # return render_template("index.html")
