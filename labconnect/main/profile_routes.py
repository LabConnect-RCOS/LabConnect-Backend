from flask import jsonify, request, Response, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from labconnect import db
from labconnect.models import User, UserDepartments, UserMajors, Departments, Majors
from . import main_blueprint

def user_to_dict(user: User) -> dict:
    """ Helper function to serialize User object data. """
    user_departments = db.session.execute(
        db.select(UserDepartments.department_id).where(UserDepartments.user_id == user.id)
    ).scalars().all()

    user_majors = db.session.execute(
        db.select(UserMajors.major_code).where(UserMajors.user_id == user.id)
    ).scalars().all()

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "preferred_name": user.preferred_name,
        "class_year": user.class_year,
        "profile_picture": user.profile_picture,
        "website": user.website,
        "description": user.description,
        "departments": user_departments,
        "majors": user_majors,
    }

@main_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def get_profile() -> Response:
    """ GET /profile: current user profile """
    user_email = get_jwt_identity()
    user = db.session.execute(db.select(User).where(User.email == user_email)).scalar_one_or_none()

    if not user:
        return make_response(jsonify({"msg": "User not found"}), 404)

    return jsonify(user_to_dict(user))

@main_blueprint.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile() -> Response:
    """ PUT /profile: Updates current user profile """
    user_email = get_jwt_identity()
    user = db.session.execute(db.select(User).where(User.email == user_email)).scalar_one_or_none()

    if not user:
        return make_response(jsonify({"msg": "User not found"}), 404)

    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"msg": "Missing JSON in request"}), 400)

    # Update basic User fields
    user.first_name = json_data.get("first_name", user.first_name)
    user.last_name = json_data.get("last_name", user.last_name)
    user.preferred_name = json_data.get("preferred_name", user.preferred_name)
    user.class_year = json_data.get("class_year", user.class_year)
    user.website = json_data.get("website", user.website)
    user.description = json_data.get("description", user.description)

    db.session.commit()

    return jsonify({"msg": "Profile updated successfully"})
