from flask import Response, make_response, render_template

from . import error_blueprint


@error_blueprint.app_errorhandler(404)
def page_not_found(e) -> Response:
    # 404 error page
    return make_response(render_template("404.html"), 404)


@error_blueprint.app_errorhandler(500)
def error_for_server(e) -> Response:
    # 500 error page
    return make_response(render_template("500.html"), 500)
