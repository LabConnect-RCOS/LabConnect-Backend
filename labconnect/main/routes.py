from typing import Any
from flask import abort, request

from labconnect import db
from labconnect.helpers import SemesterEnum
from labconnect.models import (
    ClassYears,
    Courses,
    LabManager,
    Leads,
    Majors,
    Opportunities,
    RecommendsClassYears,
    RecommendsCourses,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
)

from . import main_blueprint

# Example queries
# @main_blueprint.route("/test")
# def test():
#     query = (
#         db.session.query(Opportunities, Majors)
#         .filter(Majors.major_code == "CSCI")
#         .join(RecommendsMajors, Majors.major_code == RecommendsMajors.major_code)
#         .join(Opportunities, Opportunities.id == RecommendsMajors.opportunity_id)
#     )
#     query = (
#         db.session.query(Opportunities, Majors)
#         .filter(Opportunities.id == 2)
#         .join(RecommendsMajors, Opportunities.id == RecommendsMajors.opportunity_id)
#         .join(Majors, RecommendsMajors.major_code == Majors.major_code)
#     )
#     print(query)
#     data = query.all()
#     print(data)
#     return {"Hello": "There"}


@main_blueprint.route("/")
def index():
    return {"Hello": "There"}


@main_blueprint.route("/opportunities")
def positions():
    return {"Hello": "There"}


@main_blueprint.route("/opportunity/<int:id>")
def opportunity(id: int):
    return {"Hello": "There"}


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return {"Hello": "There"}


@main_blueprint.route("/department")
def department():

    if not request.data:
        abort(400)

    department = request.get_json().get("department", None)

    if not department:
        abort(400)

    # departmentOf department_name
    department_data = db.first_or_404(
        db.select(RPIDepartments, RPISchools.name)
        .filter(RPIDepartments.name == department)
        .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
    )

    # professors = request.get_json().get("labmanagers", None)

    # professors = (
    # db.session.query(
    # Need all professors first
    # RPIDepartments.lab_managers
    # )
    # now old format look bellow for new way to do
    # Professors department needs to match department (data[0])
    # .filter(RPIDepartments.name == data[0])
    # .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
    # ).first()

    # print(data)

    # rpidepartment.name

    # combine with professor dictionary
    result = department_data.to_dict()

    print(result)

    # Might not need
    if not request.data:
        abort(400)

    professors = request.get_json().get("department", None)

    if not professors:
        abort(400)

    # departmentOf department_name
    prof_data = db.first_or_404(
        db.select(RPIDepartments, LabManager.name).filter(
            LabManager.department_id == result[0]
        )
        # RPIDepartments.name == result[0]
        # .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
        .join(
            RPIDepartments, LabManager.rcs_id, LabManager.name, LabManager.department_id
        )
        # rcs_id=row_tuple[0], name=row_tuple[1], department_id=row_tuple[2]
        # , RPIDepartments.school_id == RPISchools.name)
    )
    result2 = prof_data.to_dict()
    # return result2?

    return result


@main_blueprint.route("/discover")
def discover():
    return {"Hello": "There"}


@main_blueprint.route("/getOpportunity/<string:opp_id>", methods=["GET"])
def getOpportunity(opp_id: str):
    if request.method == "GET":
        # query database for opportunity

        # return data in the below format if opportunity is found
        return {
            "id": "u1",
            "title": "Software Engineer",
            "department": "Computer Science",
            "location": "Sage Hall",
            "date": "2024-02-23",
            "author": "John Doe",
            "credits": 2,
            "description": "This is a description",
            "salary": 15,
            "upfrontPay": 200,
            "years": ["Freshman", "Junior", "Sophomore"],
        }

    abort(500)


@main_blueprint.route("/getProfessorProfile/<string:rcs_id>", methods=["GET"])
def getProfessorProfile(rcs_id: str):
    # test code until database code is added
    if request.method == "GET":
        return {
            "name": "Peter Johnson",
            "image": "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
            "researchCenter": "Computational Fake Center",
            "department": "Computer Science",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
        pharetra sit amet aliquam id diam maecenas ultricies mi. Montes
        nascetur ridiculus mus mauris vitae ultricies leo. Porttitor massa
        id neque aliquam. Malesuada bibendum arcu vitae elementum. Nulla
        aliquet porrsus mattis molestie aiaculis at erat pellentesque. 
        At risus viverra adipiscing at.
        Tincidunt tortor aliquam nulla facilisi cras fermentum odio eu
        feugiat. Eget fUt eu sem integer vitae justo
        eget magna fermentum. Lobortis feugiat vivamus at augue eget arcu
        dictum. Et tortor at risus viverra adipiscing at in tellus.
        Suspendisse sed nisi lacus sed viverra tellus. Potenti nullam ac
        tortor vitae. Massa id neque aliquam vestibulum. Ornare arcu odio ut
        sem nulla pharetra. Quam id leo in vitae turpis massa. Interdum
        velit euismod in pellentesque massa placerat duis ultricies lacus.
        Maecenas sed enim ut sem viverra aliquet eget sit amet. Amet
        venenatis urna cursus eget nunc scelerisque viverra mauris. Interdum
        varius sit amet mattis. Aliquet nec ullamcorper sit amet risus
        nullam. Aliquam faucibus purus in massa tempor nec feugiat. Vitae
        turpis massa sed elementum tempus. Feugiat in ante metus dictum at
        tempor. Malesuada nunc vel risus commodo viverra maecenas accumsan.
        Integer vitae justo.""",
        }

    abort(500)


@main_blueprint.route("/getProfessorOpportunityCards/<string:rcs_id>", methods=["GET"])
def getProfessorOpportunityCards(rcs_id: str):
    # test code until database code is added
    if request.method == "GET":

        # query database for opportunities

        # return opportunities
        return {
            rcs_id: [
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o1",
                },
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o2",
                },
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o3",
                },
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o4",
                },
            ]
        }
    abort(500)


@main_blueprint.route("/getProfessorMeta", methods=["GET"])
def getProfessorMeta():
    if request.method == "GET":
        data = request.json

        user_id = data["user_id"]
        auth_token = data["authToken"]

        # query database to match user id and password from data received

        # if match, return user data
        # more fields to be added here later

        return {
            "name": "Dr. Peter Johnson",
            "department": "Computer Science",
            "researchCenter": "Computational Fake Center",
            "email": "johnj@rpi.edu",
            "phone": "518-123-4567",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do""",
            "image": "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
        }

    abort(500)


# _______________________________________________________________________________________________#

# Editing Opportunities in Profile Page


@main_blueprint.route("/deleteOpportunity", methods=["DELETE", "POST"])
def deleteOpportunity():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        postID = data["postID"]
        authToken = data["authToken"]
        authorID = data["authToken"]

        # query database to see if the credentials above match

        # if match is found, delete the opportunity, return status 200

        abort(200)

    abort(500)


@main_blueprint.route("/changeActiveStatus", methods=["DELETE", "POST"])
def changeActiveStatus():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        postID = data["postID"]
        authToken = data["authToken"]
        authorID = data["authToken"]
        setStatus = data["setStatus"]

        # query database to see if the credentials above match

        # if match is found, change the opportunities active status to true or false based on setStatus

        abort(200)

    abort(500)


@main_blueprint.route("/create_post", methods=["POST"])
def create_post():
    return {"Hello": "There"}


@main_blueprint.route("/login")
def login():
    return {"Hello": "There"}


@main_blueprint.route("/500")
def force_error():
    abort(500)


@main_blueprint.get("/schools")
def schools() -> list[Any]:

    data = db.session.execute(db.select(RPISchools).order_by(RPISchools.name)).scalars()
    result = [school.to_dict() for school in data]

    return result


@main_blueprint.get("/departments")
def departments() -> list[Any]:

    data = db.session.execute(
        db.select(RPIDepartments).order_by(RPIDepartments.name)
    ).scalars()
    result = [department.to_dict() for department in data]

    return result


@main_blueprint.get("/majors")
def majors() -> list[Any]:

    if request.data:
        partial_key = request.get_json().get("input", None)

        data = db.session.execute(
            db.select(Majors)
            .order_by(Majors.code)
            .filter(
                (Majors.code.ilike(f"%{partial_key}%"))
                | (Majors.name.ilike(f"%{partial_key}%"))
            )
        ).scalars()
        result = [major.to_dict() for major in data]

        return result

    data = db.session.execute(db.select(Majors).order_by(Majors.code)).scalars()
    result = [major.to_dict() for major in data]

    return result


@main_blueprint.get("/years")
def years() -> list[Any]:

    data = db.session.execute(
        db.select(ClassYears)
        .order_by(ClassYears.class_year)
        .filter(ClassYears.active == True)
    ).scalars()
    result = [year.class_year for year in data]

    return result


@main_blueprint.get("/courses")
def courses() -> list[Any]:
    if not request.data:
        abort(400)

    partial_key = request.get_json().get("input", None)

    if not partial_key:
        abort(400)

    data = db.session.execute(
        db.select(Courses)
        .order_by(Courses.code)
        .filter(
            (Courses.code.ilike(f"%{partial_key}%"))
            | (Courses.name.ilike(f"%{partial_key}%"))
        )
    ).scalars()

    result = [course.to_dict() for course in data]

    return result
