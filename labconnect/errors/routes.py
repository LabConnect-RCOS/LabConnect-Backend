from flask import Response, make_response, render_template

from . import error_blueprint


@error_blueprint.app_errorhandler(404)
def handle_404(e) -> Response:
    # 404 error page
    return make_response({"error": "404 not found"}, 404)


@error_blueprint.app_errorhandler(500)
def handle_500(e) -> Response:
    # 500 error page
    return make_response(
        {
            "error": "500 server error. You can report issues here: https://github.com/RafaelCenzano/LabConnect/issues"
        },
        500,
    )
