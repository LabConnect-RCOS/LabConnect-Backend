from typing import Any

from flask import abort, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from labconnect import db
from labconnect.models import (
    ClassYears,
    Courses,
    LabManager,
    Leads,
    Majors,
    Opportunities,
    Participates,
    RecommendsClassYears,
    RecommendsCourses,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
    User,
    UserCourses,
    UserDepartments,
    UserMajors,
)

from . import main_blueprint


@main_blueprint.get("/")
def index():
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


# @main_blueprint.get("/getSchoolsAndDepartments/")
# def getSchoolsAndDepartments():
#     data = db.session.execute(
#         db.select(RPISchools, RPIDepartments).join(
#             RPIDepartments, RPISchools.name == RPIDepartments.school_id
#         )
#     ).scalars()

#     dictionary = {}
#     for item in data:
#         if item[0].name not in dictionary:
#             dictionary[item[0].name] = []
#         dictionary[item[0].name].append(item[1].name)

#     return dictionary


# @main_blueprint.get("/getOpportunitiesRaw/<int:id>")
# def getOpportunitiesRaw(id: int):
#     data = db.session.execute(
#         db.select(
#             Opportunities,
#             Leads,
#             LabManager,
#             RecommendsMajors,
#             RecommendsCourses,
#             RecommendsClassYears,
#         )
#         .where(Opportunities.id == id)
#         .join(Leads, Leads.opportunity_id == Opportunities.id)
#         .join(LabManager, Leads.lab_manager_id == LabManager.id)
#         .join(RecommendsMajors, RecommendsMajors.opportunity_id == Opportunities.id)
#         .join(RecommendsCourses, RecommendsCourses.opportunity_id == Opportunities.id)
#         .join(
#             RecommendsClassYears,
#             RecommendsClassYears.opportunity_id == Opportunities.id,
#         )
#     ).scalars()

#     opportunities = [opportunity.to_dict() for opportunity in data]

#     return {"data": opportunities}


# @main_blueprint.get("/lab_manager")
# def getLabManagers():
#     if not request.data:
#         abort(400)

#     json_request_data = request.get_json()

#     if not json_request_data:
#         abort(400)

#     rcs_id = json_request_data.get("rcs_id", None)

#     if not rcs_id:
#         abort(400)

#     data = db.first_or_404(db.select(LabManager).where(LabManager.id == rcs_id))

#     result = data.to_dict()

#     return result


@main_blueprint.get("/profile")
def profile():
    request_data = request.get_json()
    id = request_data.get("id", None)

    # TODO: Fix to a join query
    lab_manager = db.first_or_404(db.select(LabManager).where(LabManager.id == id))
    user = db.first_or_404(db.select(User).where(User.lab_manager_id == id))

    result = lab_manager.to_dict() | user.to_dict()

    data = db.session.execute(
        db.select(Opportunities, Leads)
        .where(Leads.lab_manager_id == lab_manager.id)
        .join(Opportunities, Leads.opportunity_id == Opportunities.id)
    ).scalars()

    result["opportunities"] = [opportunity.to_dict() for opportunity in data]

    return result


@main_blueprint.get("/staff/<string:id>")
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
    }

    return result


# @main_blueprint.get("/lab_manager/opportunities")
# def getLabManagerOpportunityCards() -> dict[Any, list[Any]]:
#     if not request.data:
#         abort(400)

#     rcs_id = request.get_json().get("rcs_id", None)

#     if not rcs_id:
#         abort(400)

#     data = db.session.execute(
#         db.select(Opportunities, LabManager)
#         .where(LabManager.id == rcs_id)
#         .join(Leads, LabManager.id == Leads.lab_manager_id)
#         .join(Opportunities, Leads.opportunity_id == Opportunities.id)
#         .order_by(Opportunities.id)
#     ).scalars()

#     if not data:
#         abort(404)

#     result = {rcs_id: [opportunity.to_dict() for opportunity in data]}

#     return result


# _______________________________________________________________________________________________#


# Editing Opportunities in Profile Page
# @main_blueprint.get("/getProfessorCookies/<string:id>")
# def getProfessorCookies(id: str):

#     # this is already restricted to "GET" requests

#     # TODO: Use JOIN query
#     lab_manager = db.first_or_404(db.select(LabManager).where(LabManager.id == id))
#     user = db.first_or_404(db.select(User).where(User.lab_manager_id == id))

#     dictionary = lab_manager.to_dict() | user.to_dict()

#     dictionary["role"] = "admin"
#     dictionary["researchCenter"] = "AI"
#     dictionary["loggedIn"] = True

#     return dictionary


# @main_blueprint.get("/getStaff/<string:department>")
# def getStaff(department: str):
#     query = db.session.execute(
#         db.select(LabManager).filter(LabManager.department_id == department)
#     )
#     data = query.all()
#     dictionary = {}
#     for item in data:
#         dictionary[item[0].rcs_id] = item[0].to_dict()
#         dictionary[item[0].rcs_id].pop("rcs_id")

# return dictionary


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


# @main_blueprint.post("/create_post")
# def create_post():
#     return {"Hello": "There"}


@main_blueprint.get("/500")
def force_error():
    abort(500)


# @main_blueprint.get("/schools")
# def schools() -> list[Any]:

#     data = db.session.execute(db.select(RPISchools).order_by(RPISchools.name)).scalars()

#     if not data:
#         abort(404)

#     result = [school.to_dict() for school in data]

#     return result


# @main_blueprint.get("/departmentsList")
# def departments() -> list[Any]:

#     data = db.session.execute(
#         db.select(RPIDepartments).order_by(RPIDepartments.name)
#     ).scalars()

#     if not data:
#         abort(404)

#     result = [department.to_dict() for department in data]

#     return result


# @main_blueprint.get("/majors")
# def majors() -> list[Any]:

#     if request.data:

#         json_request_data = request.get_json()

#         if not json_request_data:
#             abort(400)

#         partial_key = json_request_data.get("input", None)

#         data = db.session.execute(
#             db.select(Majors)
#             .order_by(Majors.code)
#             .where(
#                 (Majors.code.ilike(f"%{partial_key}%"))
#                 | (Majors.name.ilike(f"%{partial_key}%"))
#             )
#         ).scalars()

#         if not data:
#             abort(404)

#         result = [major.to_dict() for major in data]

#         return result

#     data = db.session.execute(db.select(Majors).order_by(Majors.code)).scalars()

#     if not data:
#         abort(404)

#     result = [major.to_dict() for major in data]

#     return result


# @main_blueprint.get("/years")
# def years() -> list[Any]:

#     data = db.session.execute(
#         db.select(ClassYears)
#         .order_by(ClassYears.class_year)
#         .where(ClassYears.active == True)
#     ).scalars()

#     if not data:
#         abort(404)

#     result = [year.class_year for year in data]

#     if result == []:
#         abort(404)

#     return result


# @main_blueprint.get("/courses")
# def courses() -> list[Any]:
#     if not request.data:
#         abort(400)

#     json_request_data = request.get_json()

#     if not json_request_data:
#         abort(400)

#     partial_key = json_request_data.get("input", None)

#     if not partial_key or not isinstance(partial_key, str):
#         abort(400)

#     data = db.session.execute(
#         db.select(Courses)
#         .order_by(Courses.code)
#         .where(
#             (Courses.code.ilike(f"%{partial_key}%"))
#             | (Courses.name.ilike(f"%{partial_key}%"))
#         )
#     ).scalars()

#     if not data:
#         abort(404)

#     result = [course.to_dict() for course in data]

#     if result == []:
#         abort(404)

#     return result


# @main_blueprint.get("/user")
# def user():
#     if not request.data:
#         abort(400)

#     id = request.get_json().get("id", None)

#     if not id:
#         abort(400)

#     # Query for user
#     user = db.first_or_404(db.select(User).where(User.id == id))
#     result = user.to_dict()

#     # Query for user's department(s)
#     user_departments = db.session.execute(
#         db.select(UserDepartments).where(UserDepartments.user_id == id)
#     ).scalars()
#     result["departments"] = [dept.to_dict() for dept in user_departments]

#     # Query for user's major(s)
#     user_majors = db.session.execute(
#         db.select(UserMajors).where(UserMajors.user_id == id)
#     ).scalars()
#     result["majors"] = [major.to_dict() for major in user_majors]

#     # Query for user's courses
#     user_courses = db.session.execute(
#         db.select(UserCourses)
#         .order_by(UserCourses.in_progress)
#         .where(UserCourses.user_id == id)
#     ).scalars()
#     result["courses"] = [course.to_dict() for course in user_courses]

#     # Query for user's opportunities
#     user_opportunities = db.session.execute(
#         db.select(Opportunities, Participates)
#         .where(Participates.user_id == id)
#         .join(Opportunities, Participates.opportunity_id == Opportunities.id)
#         .order_by(Opportunities.active.desc())
#     ).scalars()
#     result["opportunities"] = [
#         opportunity.to_dict() for opportunity in user_opportunities
#     ]

#     return result
