from datetime import datetime, timedelta, timezone

from uuid import uuid4
import hashlib

import logging
from sqlalchemy.exc import SQLAlchemyError

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
        #Assuming RPI email
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

#New user
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
    user.majors = json_data.get("majors", "")
    user.courses = json_data.get("course", "")
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
        # permissions = json_data["permissions"]
        management_permissions = ManagementPermissions()
        management_permissions.user_id = user.id
        # management_permissions.all_admin = permissions.get("all_admin", False)
        # management_permissions.admin = permissions.get("admin", False)
        # management_permissions.moderator = permissions.get("moderator", False)
        management_permissions.all_admin = False
        management_permissions.admin = False
        management_permissions.moderator = False
        db.session.add(management_permissions)

    db.session.commit()
    return make_response({"msg": "New user added"})

#This could possibly be done here
#Create a way to invite people  (end 7/25)
#Current plan: a system that can create an invite link, hash the email (or something else) and then get a special link

#some possible ideas
@main_blueprint.post("/invite")
def invite_user() -> Response:
    json_data = request.get_json()
    if not json_data:
        abort(400)

    #user = User()
    recipient_email = json_data.get("email")

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)

    #need later?
    token_hash = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    invite = InviteToken(
        email=recipient_email,
        token_hash=token_hash,
        expires_at=expires_at
    )

    invite_link = f"{current_app.config['FRONTEND_URL']}/invite/?token={invite}"
    #Need to confirm whitch one works better
    invite_link = f"{current_app.config['FRONTEND_URL']}/invite/?token={InviteToken}"

    #return make_response({"invite_link": invite_link}, 200)

    holdId = id
    holdEmail = email

    return invite

#Make token
class InviteToken(db.Model):
    __tablename__ = "invite_tokens"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    token_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)

@main_blueprint.post("/invite")
@jwt_required()  
# only logged in users should be able to invite
def invite_user() -> Response:
    json_data = request.get_json()
    if not json_data or "email" not in json_data:
        return make_response({"msg": "Missing email"}, 400) 

    recipient_email = json_data["email"].strip().lower()


    # Create  token
    token = str(uuid4())
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    # Token valid for 24 hrs (can change)
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)

    # Save to DB
    invite = InviteToken(
        email=recipient_email,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.session.add(invite)
    db.session.commit()

    # Construct invite link (send this to frontend for email distribution)
    #would need more work
    invite_link = f"{current_app.config['FRONTEND_URL']}/invite/?token={token}"

    return make_response({"invite_link": invite_link}, 200)

#Validate token
def validate_invite_token(token: str) -> str | None:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    invite = db.session.execute(
        db.select(InviteToken).where(InviteToken.token_hash == token_hash)
    ).scalar()
    
    if invite and invite.expires_at > datetime.now(timezone.utc) and not invite.used:
        return invite.email

    return None

def cleanup_expired_invites():
    now = datetime.now(timezone.utc)
    db.session.execute(
        db.delete(InviteToken).where(InviteToken.expires_at < now)
    )
    db.session.commit()

def check_token(token: str):
    token_hold

    # Convert the token string to bytes
    token_bytes = token.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the token bytes
    sha256_hash.update(token_bytes)

    # Get the hexadecimal digest
    token_hold = sha256_hash.hexdigest()

    invite = db.session.execute(
        db.select(InviteToken).where(InviteToken.token_hash == token_hold)
    ).scalar()

    if invite and invite.expires_at > datetime.datetime.timezone.et():
        return invite.email
    return None

#//////////////////////////////////////////////////////////////////



#Validate token
def validate_Tk(token: str) -> str | None:
    tk_hash = hashlib.sha256(token.encode()).hexdigest()
    invite = db.session.execute(
        db.select(InviteToken).where(InviteToken.tk_hash == tk_hash)
    ).scalar()
    #Proper time zone
    if invite and invite.expires_at > datetime.datetime.timezone.et():
        return invite.email
    return None


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

#registration routes 
#Create/fix the registration backend routes. When someone logs in for the first time we need information about the user  (end of 6/25 to mid 7/25)
#Name, class year, major, RPI email, ect
#Need to ask how to check my work

@main_blueprint.post("/register")
def register_user() -> Response:
    # parse data
    json_data = request.get_json()
    if not json_data:
        return make_response({"msg": "Missing user data"}, 400)

    # Required fields (may need more)
    if "email" not in json_data:
        return make_response({"msg": "Missing required field: email"}, 400)\
        
    existing_user = User.query.filter_by(email=json_data["email"]).first()
    if existing_user:
        return make_response({"msg": "User already registered"}, 409)
    
    if not json_data["email"].endswith("@rpi.edu"):
        return make_response({"msg": "Must use RPI email address"}, 400)
    
    # majors, courses, departments need to always be lists
    majors = json_data.get("majors", [])
    if isinstance(majors, str):
        majors = [majors]

    courses = json_data.get("courses", [])
    if isinstance(courses, str):
        courses = [courses]

    departments = json_data.get("departments", [])
    if isinstance(departments, str):
        departments = [departments]

    try:
        # Create new User object
        user = User(
            email=json_data.get("email"),
            first_name=json_data.get("first_name"),
            last_name=json_data.get("last_name"),
            preferred_name=json_data.get("preferred_name", ""),
            class_year=json_data.get("class_year", ""),
            majors=",".join(majors),  # If storing as comma string
            courses=",".join(courses),  # If storing as comma string
            profile_picture=json_data.get(
                "profile_picture",
                "https://www.svgrepo.com/show/206842/professor.svg"
            ),
            website=json_data.get("website", ""),
            description=json_data.get("description", "")
        )
        db.session.add(user)
        db.session.flush()  # to get user.id before adding relationships

        # Add departments
        for department_id in departments:
            db.session.add(UserDepartments(
                user_id=user.id,
                department_id=department_id
            ))

        # Add majors 
        for major_code in majors:
            db.session.add(UserMajors(
                user_id=user.id,
                major_code=major_code
            ))

        # Add courses
        for course_code in courses:
            db.session.add(UserCourses(
                user_id=user.id,
                course_code=course_code
            ))

        # Add default permissions
        # Possibly auto-assign moderator/admin based on department or role
        db.session.add(ManagementPermissions(
            user_id=user.id,
            all_admin=False,
            admin=False,
            moderator=False
        ))

        # 5. Commit transaction
        db.session.commit()

        # 6. Log registration
        logging.info(f"New user registered: {user.email}")

        return make_response({"msg": "New user added successfully"}, 201)

    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response({"msg": "Registration failed", "error": str(e)}, 500)
    
    # Create new User 
    user = User(
        email=json_data.get("email"),
        first_name=json_data.get("first_name"),
        last_name=json_data.get("last_name"),
        preferred_name=json_data.get("preferred_name", ""),
        class_year=json_data.get("class_year", ""),
        majors=json_data.get("majors", ""),  # stored as string now may make list
        courses=json_data.get("course", ""),  # stored as string now may make list too
        profile_picture=json_data.get(
            "profile_picture",
            "https://www.svgrepo.com/show/206842/professor.svg"
        ),
        website = json_data.get("website", ""),
        description = json_data.get("description", "")
    )
    db.session.add(user)
    db.session.commit()  # commit so user.id is available

    # Add departments (if given)
    departments = json_data.get("departments", [])
    for department_id in departments:
        db.session.add(UserDepartments(
            user_id=user.id,
            department_id=department_id
        ))

    #Add majors (if given as a list)
    majors = json_data.get("majors", [])
    for major_code in majors:
        db.session.add(UserMajors(
            user_id=user.id,
            major_code=major_code
        ))

    # Add courses (if given as a list)
    courses = json_data.get("courses", [])
    for course_codes in courses:
        db.session.add(UserCourses(
            user_id=user.id,
            course_code=course_codes
        ))

    # Set permissions 
    db.session.add(ManagementPermissions(
        user_id=user.id,
        all_admin=False,
        admin=False,
        moderator=False
    ))

   
    db.session.commit()

    return make_response({"msg": "New user added successfully"}, 201)
#//////////////////////////////////////
#Not exactly sure where this should go but its going here for now

from labconnect import db
from datetime import datetime

class LabGroup(db.Model):
    __tablename__ = "lab_groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)  # relates to course
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    creator = db.relationship("User", backref="created_lab_groups")
    members = db.relationship(
        "User",
        secondary="lab_group_members",
        back_populates="lab_groups"
    )

class LabGroupMembers(db.Model):
    __tablename__ = "lab_group_members"
    lab_group_id = db.Column(db.Integer, db.ForeignKey("lab_groups.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

# Add back-populate on User model if not present:
User.lab_groups = db.relationship(
    "LabGroup",
    secondary="lab_group_members",
    back_populates="members"
)

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify

@main_blueprint.post("/labgroups/create")
@jwt_required()
def create_lab_group():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Only professors (or users with admin/moderator perms) can create lab groups
    perms = ManagementPermissions.query.filter_by(user_id=user.id).first()
    if not perms or not (perms.admin or perms.moderator):
        return jsonify({"msg": "Permission denied"}), 403

    data = request.get_json()
    name = data.get("name")
    course_code = data.get("course_code")

    if not name or not course_code:
        return jsonify({"msg": "Missing lab group name or course_code"}), 400

    # Optional: Check if course_code is valid for this professor

    lab_group = LabGroup(
        name=name,
        course_code=course_code,
        creator_id=user.id
    )
    db.session.add(lab_group)
    db.session.commit()

    return jsonify({
        "msg": "Lab group created",
        "lab_group_id": lab_group.id,
        "name": lab_group.name,
        "course_code": lab_group.course_code
    }), 201

@main_blueprint.post("/labgroups/<int:lab_group_id>/add_member")
@jwt_required()
def add_member_to_lab_group(lab_group_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    lab_group = LabGroup.query.get(lab_group_id)
    if not lab_group:
        return jsonify({"msg": "Lab group not found"}), 404

    # Only creator or admin/moderator can add members
    perms = ManagementPermissions.query.filter_by(user_id=user.id).first()
    if user.id != lab_group.creator_id and not (perms and (perms.admin or perms.moderator)):
        return jsonify({"msg": "Permission denied"}), 403

    data = request.get_json()
    member_email = data.get("email")
    if not member_email:
        return jsonify({"msg": "Missing member email"}), 400

    member = User.query.filter_by(email=member_email).first()
    if not member:
        return jsonify({"msg": "Member user not found"}), 404

    if member in lab_group.members:
        return jsonify({"msg": "User already a member"}), 400

    lab_group.members.append(member)
    db.session.commit()

    return jsonify({"msg": f"Added {member_email} to lab group {lab_group.name}"}), 200


@main_blueprint.get("/labgroups")
@jwt_required()
def list_lab_groups():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Return all lab groups user is member of or created
    lab_groups = user.lab_groups + user.created_lab_groups
    lab_groups = list({lg.id: lg for lg in lab_groups}.values())  # remove duplicates

    response = [
        {
            "id": lg.id,
            "name": lg.name,
            "course_code": lg.course_code,
            "creator_id": lg.creator_id,
            "member_count": len(lg.members)
        }
        for lg in lab_groups
    ]
    return jsonify(response), 200
