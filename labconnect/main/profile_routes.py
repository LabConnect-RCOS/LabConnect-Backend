from flask import Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from sqlalchemy import select, delete

from labconnect import db
from labconnect.models import Majors, RPIDepartments, User, UserDepartments, UserMajors

from . import main_blueprint


def user_to_dict(user: User) -> dict:
    """Helper function to serialize User object data."""
    user_departments = (
        db.session.execute(
            select(UserDepartments.department_id).where(
                UserDepartments.user_id == user.id
            )
        )
        .scalars()
        .all()
    )

    user_majors = (
        db.session.execute(
            select(UserMajors.major_code).where(UserMajors.user_id == user.id)
        )
        .scalars()
        .all()
    )

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
    """GET /profile: current user profile"""
    user_email = get_jwt_identity()
    user = db.session.execute(
        select(User).where(User.email == user_email)
    ).scalar_one_or_none()

    if not user:
        return {"msg": "User not found"}, 404

    return jsonify(user_to_dict(user))


@main_blueprint.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile() -> Response:
    """PUT /profile: Updates current user profile"""
    user_email = get_jwt_identity()
    user = db.session.execute(
        select(User).where(User.email == user_email)
    ).scalar_one_or_none()

    if not user:
        return {"msg": "User not found"}, 404

    json_data = request.get_json()
    if not json_data:
        return {"msg": "Missing JSON in request"}, 400

    # Update basic User fields
    user.first_name = json_data.get("first_name", user.first_name)
    user.last_name = json_data.get("last_name", user.last_name)
    user.preferred_name = json_data.get("preferred_name", user.preferred_name)
    user.class_year = json_data.get("class_year", user.class_year)
    user.website = json_data.get("website", user.website)
    user.description = json_data.get("description", user.description)

    if "departments" in json_data:
        db.session.execute(
            delete(UserDepartments).where(UserDepartments.user_id == user.id)
        )
        
        req_dept_ids = set(json_data["departments"])
        if req_dept_ids: # Only query if list is not empty
            valid_dept_ids = db.session.execute(
                select(RPIDepartments.id).where(
                    RPIDepartments.id.in_(req_dept_ids)
                )
            ).scalars().all()

            for dept_id in valid_dept_ids: # Add only the valid ones
                new_user_dept = UserDepartments(user_id=user.id, department_id=dept_id)
                db.session.add(new_user_dept)

    if "majors" in json_data:
        db.session.execute(
            delete(UserMajors).where(UserMajors.user_id == user.id)
        )
        
        req_major_codes = set(json_data["majors"])
        if req_major_codes: # Only query if list is not empty
            valid_major_codes = db.session.execute(
                select(Majors.code).where(Majors.code.in_(req_major_codes))
            ).scalars().all()

            for major_code in valid_major_codes: # Add only the valid ones
                new_user_major = UserMajors(user_id=user.id, major_code=major_code)
                db.session.add(new_user_major)

    db.session.commit()

    return {"msg": "Profile updated successfully"}
