from typing import Any

from flask import Response, abort, request, redirect, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    unset_jwt_cookies,
)
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from labconnect import db
from labconnect.models import (
    User,
)
from labconnect.helpers import prepare_flask_request

from . import main_blueprint


@main_blueprint.route("/login")
def saml_login():
    # Initialize SAML auth request
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=current_app.config["SAML_CONFIG"])
    return redirect(auth.login())


@main_blueprint.post("/callback")
def saml_callback():
    # Process SAML response
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=current_app.config["SAML_CONFIG"])
    auth.process_response()
    errors = auth.get_errors()

    if not errors:
        user_info = auth.get_attributes()
        user_id = auth.get_nameid()

        data = db.session.execute(db.select(User).where(User.email == "email")).scalar()

        # User doesn't exist, create a new user
        if data is None:

            # TODO: add data
            user = User(
                # email=email,
                # first_name=first_name,
                # last_name=last_name,
                # preferred_name=json_request_data.get("preferred_name", None),
                # class_year=class_year,
            )

            db.session.add(user)
            db.session.commit()

        # Generate JWT
        token = create_access_token(identity=user_id)

        # Send the JWT to the frontend
        return {"token": token}
    else:
        return {"errors": errors}, 400


@main_blueprint.get("/logout")
def logout() -> Response:
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
