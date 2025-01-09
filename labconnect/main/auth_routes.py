from datetime import datetime, timedelta
from uuid import uuid4

from flask import current_app, make_response, redirect, request, abort
from flask_jwt_extended import create_access_token
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from labconnect import db
from labconnect.helpers import prepare_flask_request
from labconnect.models import (
    User,
    UserCourses,
    UserDepartments,
    UserMajors,
    ManagementPermissions,
)

from . import main_blueprint

temp_codes = {}


def generate_temporary_code(user_email: str, registered: bool) -> str:
    # Generate a unique temporary code
    code = str(uuid4())
    expires_at = datetime.now() + timedelta(seconds=5)  # expires in 5 seconds
    temp_codes[code] = {
        "email": user_email,
        "expires_at": expires_at,
        "registered": registered,
    }
    return code


def validate_code_and_get_user_email(code: str) -> tuple[str | None, bool | None]:
    token_data = temp_codes.get(code, {})
    if not token_data:
        return None, None

    user_email = token_data.get("email", None)
    expire = token_data.get("expires_at", None)
    registered = token_data.get("registered", False)

    if user_email and expire and expire > datetime.now():
        # If found, delete the code to prevent reuse
        del temp_codes[code]
        return user_email, registered
    elif expire:
        # If the code has expired, delete it
        del temp_codes[code]

    return None, None


@main_blueprint.get("/login")
def saml_login():

    # In testing skip RPI login purely for local development
    if current_app.config["TESTING"] and (
        current_app.config["FRONTEND_URL"] == "http://localhost:3000"
        or current_app.config["FRONTEND_URL"] == "http://127.0.0.1:3000"
    ):
        # Generate JWT
        code = generate_temporary_code("test@rpi.edu", True)

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
        registered = True
        user_info = auth.get_attributes()
        # user_id = auth.get_nameid()

        data = db.session.execute(db.select(User).where(User.email == "email")).scalar()

        # User doesn't exist, create a new user
        if data is None:
            registered = False
        # Generate JWT
        # token = create_access_token(identity=[user_id, datetime.now()])
        code = generate_temporary_code(user_info["email"][0], registered)

        # Send the JWT to the frontend
        return redirect(f"{current_app.config['FRONTEND_URL']}/callback/?code={code}")

    error_reason = auth.get_last_error_reason()
    return {"errors": errors, "error_reason": error_reason}, 500


@main_blueprint.post("/register")
def registerUser():

    # Gather the new user's information
    json_data = request.get_json()
    if not json_data:
        abort(400)

    user = User()
    user.email = json_data.get("email")
    user.first_name = json_data.get("first_name")
    user.last_name = json_data.get("last_name")
    user.preferred_name = json_data.get("preferred_name", "")
    user.class_year = json_data.get("class_year", "")
    user.profile_picture = json_data.get(
        "profile_picture", "https://www.svgrepo.com/show/206842/professor.svg"
    )
    user.website = json_data.get("website", "")
    user.description = json_data.get("description", "")
    db.session.add(user)
    db.session.commit()

    # Add UserDepartments if provided
    if json_data.get("departments"):
        for department_id in json_data["departments"]:
            user_department = UserDepartments()
            user_department.department_id = department_id
            user_department.user_id = user.id
            db.session.add(user_department)

    # Additional auxiliary records (majors, courses, etc.)
    if json_data.get("majors"):
        for major_code in json_data["majors"]:
            user_major = UserMajors()
            user_major.user_id = user.id
            user_major.major_code = major_code
            db.session.add(user_major)
    # Add Courses if provided
    if json_data.get("courses"):
        for course_code in json_data["courses"]:
            user_course = UserCourses()
            user_course.user_id = user.id
            user_course.course_code = course_code
            db.session.add(user_course)

    # Add ManagementPermissions if provided
    if json_data.get("permissions"):
        permissions = json_data["permissions"]
        management_permissions = ManagementPermissions()
        management_permissions.user_id = user.id
        management_permissions.super_admin = permissions.get("super_admin", False)
        management_permissions.admin = permissions.get("admin", False)
        management_permissions.moderator = permissions.get("moderator", False)
        db.session.add(management_permissions)

    db.session.commit()
    return {"msg": "New user added"}


@main_blueprint.post("/token")
def tokenRoute():
    if request.json is None or request.json.get("code", None) is None:
        return {"msg": "Missing JSON body in request"}, 400
    # Validate the temporary code
    code = request.json["code"]
    if code is None:
        return {"msg": "Missing code in request"}, 400
    user_email, registered = validate_code_and_get_user_email(code)

    if user_email is None:
        return {"msg": "Invalid code"}, 400

    token = create_access_token(identity=[user_email, datetime.now()])
    return {"token": token, "registered": registered}


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
    # TODO: add token to blacklist
    return {"msg": "logout successful"}
