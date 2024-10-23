from datetime import datetime

from flask import current_app, make_response, redirect, request
from flask_jwt_extended import create_access_token
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from labconnect import db
from labconnect.helpers import prepare_flask_request
from labconnect.models import User

from . import main_blueprint


@main_blueprint.get("/login")
def saml_login():

    if current_app.config["TESTING"]:
        # Generate JWT
        token = create_access_token(identity=["test", datetime.now()])

        # Send the JWT to the frontend
        return redirect(f"{current_app.config['FRONTEND_URL']}/?token={token}")

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
        token = create_access_token(identity=[user_id, datetime.now()])

        # Send the JWT to the frontend
        return redirect(f"{current_app.config['FRONTEND_URL']}/?token={token}")

    return {"errors": errors}, 500


@main_blueprint.get("/metadata/")
def metadataRoute():
    req = prepare_flask_request(request)
    auth = auth = OneLogin_Saml2_Auth(
        req, custom_base_path=current_app.config["SAML_CONFIG"]
    )
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers["Content-Type"] = "text/xml"
    else:
        resp = make_response(", ".join(errors), 500)
    return resp


@main_blueprint.get("/logout")
def logout():
    if not current_app.config["TESTING"]:
        # TODO: add token to blacklist
        # current_app.config["TOKEN_BLACKLIST"].add()
        pass
    return {"msg": "logout successful"}
