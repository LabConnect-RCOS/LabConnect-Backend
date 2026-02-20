# Add registration/sign up page/procedure
# Make a registration process for professors

from datetime import datetime, timedelta
from uuid import uuid4

# import flask
from flask import abort, current_app, make_response, redirect, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from werkzeug.wrappers.response import Response

from labconnect import db
from labconnect.helpers import prepare_flask_request
from labconnect.models import (
    Codes,
    ManagementPermissions,
    User,
    UserProfessor,
    UserCourses,
    UserDepartments,
    UserMajors,
)

from . import main_blueprint

temp_codes = {}


def generate_temporary_code(user_email: str, registered: bool) -> str:
    # Generate a unique temporary code
    code = str(uuid4())
    expires_at = datetime.now() + timedelta(seconds=10)  # expires in 10 seconds
    new_code = Codes()
    new_code.code = code
    new_code.email = user_email
    new_code.registered = registered
    new_code.expires_at = expires_at
    db.session.add(new_code)
    db.session.commit()
    return code


def validate_code_and_get_user_email(code: str) -> tuple[str, bool] | tuple[None, None]:
    code_data = db.session.execute(db.select(Codes).where(Codes.code == code)).scalar()
    if not code_data:
        return None, None

    user_email = code_data.email
    expire = code_data.expires_at
    registered = code_data.registered

    if user_email and expire:
        if expire > datetime.now():
            # If found, delete the code to prevent reuse
            db.session.delete(code_data)
            return user_email, registered
        else:
            # If the code has expired, delete it
            db.session.delete(code_data)

    return None, None


# Past work on rpi login


@main_blueprint.get("/login")
def saml_login() -> Response:
    # In testing skip RPI login purely for local development
    if current_app.config["TESTING"] and (
        current_app.config["FRONTEND_URL"] == "http://localhost:5173"
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
def saml_callback() -> Response:
    # Process SAML response
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=current_app.config["SAML_CONFIG"])
    auth.process_response()
    errors = auth.get_errors()

    if not errors:
        registered = True
        user_info = auth.get_attributes()
        user_id = next(iter(user_info.values()))[0] + "@rpi.edu"

        data = db.session.execute(db.select(User).where(User.email == user_id)).scalar()

        # User doesn't exist, create a new user
        if data is None:
            registered = False
        # Generate JWT
        code = generate_temporary_code(user_id, registered)

        # Send the JWT to the frontend
        return redirect(f"{current_app.config['FRONTEND_URL']}/callback/?code={code}")

    error_reason = auth.get_last_error_reason()
    return make_response({"errors": errors, "error_reason": error_reason}, 500)


@main_blueprint.post("/token")
def tokenRoute() -> Response:
    if request.json is None or request.json.get("code", None) is None:
        return make_response({"msg": "Missing JSON body in request"}, 400)

    # Validate the temporary code
    code = request.json["code"]
    if code is None:
        return make_response({"msg": "Missing code in request"}, 400)

    user_email, registered = validate_code_and_get_user_email(code)
    if user_email is None:
        return make_response({"msg": "Invalid code"}, 400)

    access_token = create_access_token(identity=user_email)
    refresh_token = create_refresh_token(identity=user_email)
    resp = make_response({"registered": registered})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


@main_blueprint.post("/register")
def registerUser() -> Response:
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
    # Place holder picture
    user.profile_picture = json_data.get(
        "profile_picture", "https://www.svgrepo.com/show/206842/professor.svg"
    )
    # Do we still need
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
        # permissions = json_data["permissions"]
        management_permissions = ManagementPermissions()
        management_permissions.user_id = user.id
        # management_permissions.super_admin = permissions.get("super_admin", False)
        # management_permissions.admin = permissions.get("admin", False)
        # management_permissions.moderator = permissions.get("moderator", False)
        management_permissions.super_admin = False
        management_permissions.admin = False
        management_permissions.moderator = False
        db.session.add(management_permissions)

    db.session.commit()
    return make_response({"msg": "New user added"})


# promotes/demotes User to a Lab Manager
# requires a super admin to promote
@main_blueprint.patch("/users/<string:email>/permissions")
@jwt_required()
def promoteUser(email: str) -> Response:
    json_data = request.json
    if not json_data or not json_data.get("change_status"):
        abort(400)

    # if user accessing doesn't have the right perms then they can't assign perms
    promoter_id = get_jwt_identity()
    promoter_perms = (
        db.session.query(ManagementPermissions).filter_by(user_id=promoter_id).first()
    )
    if not promoter_perms or not promoter_perms.super_admin:
        return make_response({"msg": "Missing permissions"}, 401)

    # look for the user that will be promoted
    manager = db.session.query(User).filter_by(email=email).first()
    if not manager:
        return make_response({"msg": "No user matches RCS ID"}, 500)

    management_permissions = (
        db.session.query(ManagementPermissions).filter_by(user_id=manager.id).first()
    )

    if management_permissions.admin:
        management_permissions.admin = False
    elif not management_permissions.admin:
        management_permissions.admin = True

    if management_permissions is None:
        management_permissions = ManagementPermissions(user_id=manager.id, admin=True)
        db.session.add(management_permissions)

    db.session.commit()

    return make_response({"msg": "User Lab Manager permissions changed!"}, 200)


@main_blueprint.get("/metadata/")
def metadataRoute() -> Response:
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


@main_blueprint.get("/authcheck")
@jwt_required()
def authcheck() -> Response:
    return make_response({"msg": "authenticated"})


@main_blueprint.get("/token/refresh")
@jwt_required(refresh=True)
def refresh() -> Response:
    # Refreshing expired Access token
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    resp = make_response({"msg": "refresh successful"})
    set_access_cookies(resp, access_token)
    return resp


@main_blueprint.get("/logout")
def logout() -> Response:
    resp = make_response({"msg": "logout successful"})
    unset_jwt_cookies(resp)
    return resp


# Would need to add next --> Make a registration process for professors
@main_blueprint.post("/registerProfessors")
def registerProfessor() -> Response:
    # Gather the new user's information
    json_data = request.get_json()
    if not json_data:
        abort(400)
    # New type of user (professor)
    user = UserProfessor()
    # user = User()
    # This could probably stay the same
    user.email = json_data.get("email")
    user.first_name = json_data.get("first_name")
    user.last_name = json_data.get("last_name")
    user.preferred_name = json_data.get("preferred_name", "")

    # user.class_year = json_data.get("class_year", "")
    # Place holder picture
    user.profile_picture = json_data.get(
        "profile_picture", "https://www.svgrepo.com/show/206842/professor.svg"
    )

    user.website = json_data.get("website", "")
    user.description = json_data.get("description", "")

    db.session.add(user)
    db.session.commit()

    # Should only be one department
    if json_data.get("department"):
        for department_id in json_data["department"]:
            user_department = UserDepartments()
            user_department.department_id = department_id
            user_department.user_id = user.id
            db.session.add(user_department)
    """
    # Additional auxiliary records (majors, courses, etc.)
    if json_data.get("majors"):
        for major_code in json_data["majors"]:
            user_major = UserMajors()
            user_major.user_id = user.id
            user_major.major_code = major_code
            db.session.add(user_major)
    """
    # Re use as courses taught might not even be nessesary

    # No major only need department
    # Courses taught:
    if json_data.get("courses(currently) taught"):
        for course_code in json_data["courses"]:
            user_course = UserCourses()
            user_course.user_id = user.id
            user_course.course_code = course_code
            db.session.add(user_course)

    # Add ManagementPermissions if provided
    if json_data.get("permissions"):
        # permissions = json_data["permissions"]
        management_permissions = ManagementPermissions()
        management_permissions.user_id = user.id
        # management_permissions.super_admin = permissions.get("super_admin", False)
        # management_permissions.admin = permissions.get("admin", False)
        # management_permissions.moderator = permissions.get("moderator", False)
        management_permissions.super_admin = False
        management_permissions.admin = False
        management_permissions.moderator = False
        management_permissions.professor = True
        db.session.add(management_permissions)
        # Add more permissions as needed

    db.session.commit()
    return make_response({"msg": "New professor added"})
