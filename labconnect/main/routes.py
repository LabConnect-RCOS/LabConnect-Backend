from typing import NoReturn
from flask import abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from labconnect import db
from labconnect.models import (
    LabManager,
    Opportunities,
    RPIDepartments,
    User,
    ClassYears,
    UserDepartments,
    Majors,
    Courses,
)
from labconnect.serializers import serialize_course

from . import main_blueprint


@main_blueprint.get("/")
def index() -> dict[str, str]:
    return {"Hello": "There"}


@main_blueprint.get("/departments")
def departmentCards():
    data = db.session.execute(
        db.select(RPIDepartments.name, RPIDepartments.school_id, RPIDepartments.id)
    ).all()
    results = [
        {
            "title": department.name,
            "department_id": department.id,
            "school": department.school_id,
            "image": "https://cdn-icons-png.flaticon.com/512/5310/5310672.png",
        }
        for department in data
    ]
    return results


@main_blueprint.get("/departments/<string:department>")
def departmentDetails(department: str):
    department_data = db.session.execute(
        db.select(
            RPIDepartments.id,
            RPIDepartments.name,
            RPIDepartments.description,
            RPIDepartments.image,
            RPIDepartments.website,
        ).where(RPIDepartments.id == department)
    ).first()

    if department_data is None:
        abort(404)

    staff_data = db.session.execute(
        db.select(
            User.id,
            User.first_name,
            User.preferred_name,
            User.last_name,
            User.profile_picture,
        )
        .join(LabManager, User.lab_manager_id == LabManager.id)
        .join(RPIDepartments, LabManager.department_id == RPIDepartments.id)
        .where(RPIDepartments.id == department)
    ).all()

    result = {
        "id": department_data[0],
        "name": department_data[1],
        "description": department_data[2],
        "image": department_data[3],
        "website": department_data[4],
        "staff": [
            {
                "name": (
                    staff[2] + " " + staff[3] if staff[2] else staff[1] + " " + staff[3]
                ),
                "id": staff[0],
                "image": staff[4],
            }
            for staff in staff_data
        ],
    }

    return result


@main_blueprint.get("/profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    data = db.session.execute(
        db.select(
            User.preferred_name,
            User.first_name,
            User.last_name,
            User.profile_picture,
            RPIDepartments.name,
            User.description,
            User.website,
            User.lab_manager_id,
            User.id,
            User.pronouns,
        )
        .where(User.email == user_id)
        .join(UserDepartments, UserDepartments.user_id == User.id)
        .join(RPIDepartments, UserDepartments.department_id == RPIDepartments.id)
    ).first()

    if not data:
        return {"error": "profile not found"}, 404

    # if data[7]:
    #     return {"lab_manager": True, "id": data[7]}

    result = {
        "id": data[8],
        "name": data[0] + " " + data[2] if data[0] else data[1] + " " + data[2],
        "image": data[3],
        "department": data[4],
        "description": data[5],
        "website": data[6],
        "pronouns": data[9],
    }

    return result


@main_blueprint.get("/staff/<string:id>")
@jwt_required()
def getProfessorProfile(id: str):
    data = db.session.execute(
        db.select(
            User.preferred_name,
            User.first_name,
            User.last_name,
            User.profile_picture,
            RPIDepartments.name,
            User.description,
            User.website,
            User.pronouns,
        )
        .where(User.id == id)
        .join(LabManager, User.lab_manager_id == LabManager.id)
        .join(RPIDepartments, LabManager.department_id == RPIDepartments.id)
    ).first()

    if not data:
        return {"error": "profile not found"}, 404

    result = {
        "name": data[0] + " " + data[2] if data[0] else data[1] + " " + data[2],
        "image": data[3],
        "department": data[4],
        "description": data[5],
        "website": data[6],
        "pronouns": data[7],
    }

    return result


@main_blueprint.post("/changeActiveStatus")
def changeActiveStatus() -> dict[str, bool]:
    data = request.get_json()
    postID = data.get("oppID")
    setStatus = data.get("setStatus")

    if not postID or not setStatus:
        abort(404)

    # query database to see if the credentials above match
    opportunity = db.first_or_404(
        db.select(Opportunities).where(Opportunities.id == postID)
    )

    opportunity.active = setStatus

    db.session.commit()

    if opportunity.active != setStatus:
        abort(500)

    # if match is found, change the opportunities active status to true or false based on setStatus
    return {"activeStatus": opportunity}


@main_blueprint.get("/500")
def force_error() -> NoReturn:
    abort(500)


@main_blueprint.get("/majors")
def majors() -> list[dict[str, str]]:
    data = db.session.execute(db.select(Majors).order_by(Majors.code)).scalars()

    if not data:
        abort(404)

    result = [{"code": major.code, "name": major.name} for major in data]

    if result == []:
        abort(404)

    return result


@main_blueprint.get("/years")
def years() -> list[int]:
    data = db.session.execute(
        db.select(ClassYears).order_by(ClassYears.class_year).where(ClassYears.active)
    ).scalars()

    if not data:
        abort(404)

    result = [year.class_year for year in data]

    if result == []:
        abort(404)

    return result


@main_blueprint.get("/courses")
def courses() -> list[str]:
    if not request.data:
        abort(400)

    json_request_data = request.get_json()

    if not json_request_data:
        abort(400)

    partial_key = json_request_data.get("input", None)

    if not partial_key or not isinstance(partial_key, str):
        abort(400)

    data = db.session.execute(
        db.select(Courses)
        .order_by(Courses.code)
        .where(
            (Courses.code.ilike(f"%{partial_key}%"))
            | (Courses.name.ilike(f"%{partial_key}%"))
        )
    ).scalars()

    if not data:
        abort(404)

    result = [serialize_course(course) for course in data]

    if result == []:
        abort(404)

    return result
