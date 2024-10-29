from datetime import datetime, timedelta
from uuid import uuid4

from flask import current_app, make_response, redirect, request
from flask_jwt_extended import create_access_token
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from labconnect import db
from labconnect.helpers import prepare_flask_request
from labconnect.models import User

from . import main_blueprint

temp_codes = {}


def generate_temporary_code(user_email: str) -> str:
    # Generate a unique temporary code
    code = str(uuid4())
    expires_at = datetime.now() + timedelta(seconds=5)  # expires in 5 seconds
    temp_codes[code] = {"email": user_email, "expires_at": expires_at}
    return code


def validate_code_and_get_user_email(code: str) -> str | None:
    token_data = temp_codes.get(code, {})
    if not token_data:
        return None

    user_email = token_data.get("email", None)
    expire = token_data.get("expires_at", None)

    if user_email and expire and expire > datetime.now():
        # If found, delete the code to prevent reuse
        del temp_codes[code]
        return user_email
    elif expire:
        # If the code has expired, delete it
        del temp_codes[code]

    return None


@main_blueprint.get("/login")
def saml_login():

    # In testing skip RPI login purely for local development
    if (
        current_app.config["TESTING"]
        and current_app.config["Frontend_URL"] == "http://localhost:3000"
    ):
        # Generate JWT
        code = generate_temporary_code("test@rpi.edu")

        # Send the JWT to the frontend
        return redirect(f"{current_app.config['FRONTEND_URL']}/callback/?code={code}")

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
        # user_id = auth.get_nameid()

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
        # token = create_access_token(identity=[user_id, datetime.now()])
        code = generate_temporary_code(user_info["email"][0])

        # Send the JWT to the frontend
        return redirect(f"{current_app.config['FRONTEND_URL']}/callback/?code={code}")

    return {"errors": errors}, 500


@main_blueprint.post("/token")
def tokenRoute():
    if request.json is None or request.json.get("code", None) is None:
        return {"msg": "Missing JSON body in request"}, 400
    # Validate the temporary code
    code = request.json["code"]
    if code is None:
        return {"msg": "Missing code in request"}, 400
    user_email = validate_code_and_get_user_email(code)

    if user_email is None:
        return {"msg": "Invalid code"}, 400

    token = create_access_token(identity=[user_email, datetime.now()])
    return {"token": token}


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
