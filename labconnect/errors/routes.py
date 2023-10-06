from flask import make_response, render_template, Response

from . import error_blueprint


@error_blueprint.errorhandler(404)
def page_not_found(e) -> Response:
    # 404 error page
    return make_response(render_template("404.html"), 404)


@error_blueprint.errorhandler(500)
def error_for_server(e) -> Response:
    # 500 error page
    return make_response(render_template("500.html"), 500)
