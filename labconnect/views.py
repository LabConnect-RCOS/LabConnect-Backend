from flask import make_response, redirect, render_template, url_for, Response

from labconnect import app

"""
Routes
"""


@app.route("/", methods=["GET"])
def index():
    # return "Hello World"
    return render_template("home.html")


"""
Error Handlers
"""


@app.errorhandler(404)
def page_not_found(e) -> Response:
    # 404 error page
    return make_response(render_template("404.html"), 404)


@app.errorhandler(500)
def error_for_server(e) -> Response:
    # 500 error page
    return make_response(render_template("500.html"), 500)
