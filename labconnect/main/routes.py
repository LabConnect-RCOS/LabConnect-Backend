import datetime

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


def packageOpportunity(opportunityInfo, professorInfo):
    data = opportunityInfo.to_dict()
    data["professor"] = professorInfo.name
    data["department"] = professorInfo.department_id

    return data


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

    # print(data)

    # professors = (
    #     db.session.query(
    #         # Need all professors
    #         RPIDepartments.name
    #     )
    #     # Professors department needs to match department (data[0])
    #     .filter(RPIDepartments.name == data[0])
    #     # .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
    # ).first()

    # rpidepartment.name

    # combine with professor dictionary
    result = department_data.to_dict()
    print(result)
    return result


@main_blueprint.route("/discover")
def discover():
    return {"Hello": "There"}


@main_blueprint.route("/getOpportunitiesRaw/<int:id>", methods=["GET"])
def getOpportunitiesRaw(id: int):
    if request.method == "GET":
        query = db.session.execute(
            db.select(
                Opportunities,
                Leads,
                LabManager,
                RecommendsMajors,
                RecommendsCourses,
                RecommendsClassYears,
            )
            .filter(Opportunities.id == id)
            .join(Leads, Leads.opportunity_id == Opportunities.id)
            .join(LabManager, Leads.lab_manager_rcs_id == LabManager.rcs_id)
            .join(RecommendsMajors, RecommendsMajors.opportunity_id == Opportunities.id)
            .join(
                RecommendsCourses, RecommendsCourses.opportunity_id == Opportunities.id
            )
            .join(
                RecommendsClassYears,
                RecommendsClassYears.opportunity_id == Opportunities.id,
            )
        )
        data = query.all()
        print(data)

        return {"data": "check terminal"}

    abort(500)


@main_blueprint.route("/getProfessorProfile/<string:rcs_id>", methods=["GET"])
def getProfessorProfile(rcs_id: str):
    # test code until database code is added
    if request.method == "GET":

        query = db.session.execute(
            db.select(LabManager).filter(LabManager.rcs_id == rcs_id)
        )

        data = query.all()[0][0]

        return data.to_dict()

        # return {
        #     "name": "Peter Johnson",
        #     "image": "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
        #     "researchCenter": "Computational Fake Center",
        #     "department": "Computer Science",
        #     "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
        # eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
        # pharetra sit amet aliquam id diam maecenas ultricies mi. Montes
        # nascetur ridiculus mus mauris vitae ultricies leo. Porttitor massa
        # id neque aliquam. Malesuada bibendum arcu vitae elementum. Nulla
        # aliquet porrsus mattis molestie aiaculis at erat pellentesque.
        # At risus viverra adipiscing at.
        # Tincidunt tortor aliquam nulla facilisi cras fermentum odio eu
        # feugiat. Eget fUt eu sem integer vitae justo
        # eget magna fermentum. Lobortis feugiat vivamus at augue eget arcu
        # dictum. Et tortor at risus viverra adipiscing at in tellus.
        # Suspendisse sed nisi lacus sed viverra tellus. Potenti nullam ac
        # tortor vitae. Massa id neque aliquam vestibulum. Ornare arcu odio ut
        # sem nulla pharetra. Quam id leo in vitae turpis massa. Interdum
        # velit euismod in pellentesque massa placerat duis ultricies lacus.
        # Maecenas sed enim ut sem viverra aliquet eget sit amet. Amet
        # venenatis urna cursus eget nunc scelerisque viverra mauris. Interdum
        # varius sit amet mattis. Aliquet nec ullamcorper sit amet risus
        # nullam. Aliquam faucibus purus in massa tempor nec feugiat. Vitae
        # turpis massa sed elementum tempus. Feugiat in ante metus dictum at
        # tempor. Malesuada nunc vel risus commodo viverra maecenas accumsan.
        # Integer vitae justo.""",
        # }

    abort(500)


@main_blueprint.route("/getOpportunity/<int:opp_id>", methods=["GET"])
def getOpportunity(opp_id: int):
    # query database for opportunity
    query = db.session.execute(
        db.select(Opportunities, Leads, LabManager)
        .filter(Opportunities.id == opp_id)
        .join(Leads, Leads.opportunity_id == Opportunities.id)
        .join(LabManager, Leads.lab_manager_rcs_id == LabManager.rcs_id)
    )
    data = query.all()

    # check if opportunity exists
    if not data or len(data) == 0:
        abort(404)

    data = data[0]

    oppData = packageOpportunity(data[0], data[2])

    # return data in the below format if opportunity is found
    return {"data": oppData}


@main_blueprint.route("/getProfessorOpportunityCards/<string:rcs_id>", methods=["GET"])
def getProfessorOpportunityCards(rcs_id: str):
    if request.method == "GET":
        # query database for opportunity

        query = db.session.execute(
            db.select(Opportunities, Leads)
            .filter(Leads.lab_manager_rcs_id == rcs_id)
            .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        )

        data = query.all()

        cards = {"data": []}

        for row in data:
            opportunity = row[0]

            if not opportunity.active:
                continue

            oppData = {
                "id": opportunity.id,
                "title": opportunity.name,
                "body": "Due " + str(opportunity.application_due),
                "attributes": [],
            }

            if opportunity.pay > 0:
                oppData["attributes"].append("Paid")
            if int(opportunity.credits) > 0:
                oppData["attributes"].append("Credits")

            cards["data"].append(oppData)

        # return data in the below format if opportunity is found
        return cards

    abort(500)


@main_blueprint.route("/getProfileOpportunities/<string:rcs_id>", methods=["GET"])
def getProfileOpportunities(rcs_id: str):
    if request.method == "GET":
        # query database for opportunity

        query = db.session.execute(
            db.select(Opportunities, Leads)
            .filter(Leads.lab_manager_rcs_id == rcs_id)
            .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        )

        data = query.all()

        cards = {"data": []}

        for row in data:
            opportunity = row[0]

            if not opportunity.active:
                continue

            oppData = {
                "id": opportunity.id,
                "title": opportunity.name,
                "body": "Due " + str(opportunity.application_due),
                "attributes": [],
                "activeStatus": opportunity.active,
            }

            if opportunity.pay > 0:
                oppData["attributes"].append("Paid")
            if int(opportunity.credits) > 0:
                oppData["attributes"].append("Credits")

            cards["data"].append(oppData)

        # return data in the below format if opportunity is found
        return cards

    abort(500)


@main_blueprint.route("/getOpportunityByProfessor/<string:rcs_id>", methods=["GET"])
def getOpportunityByProfessor(rcs_id: str):
    if request.method == "GET":
        # query database for opportunity
        query = db.session.execute(
            db.select(Opportunities, Leads)
            .filter(Leads.lab_manager_rcs_id == rcs_id)
            .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        )

        data = query.all()
        print(data)

        # return data in the below format if opportunity is found
        return {"data": [opportunity[0].to_dict() for opportunity in data]}

    abort(500)


@main_blueprint.route("/getOpportunities", methods=["GET"])
def getOpportunities():
    if request.method == "GET":
        # query database for opportunity
        query = db.session.execute(
            db.select(Opportunities, Leads, LabManager)
            .join(Leads, Leads.opportunity_id == Opportunities.id)
            .join(LabManager, Leads.lab_manager_rcs_id == LabManager.rcs_id)
        )
        data = query.all()
        print(data[0])

        # return data in the below format if opportunity is found
        return {
            "data": [
                packageOpportunity(opportunity[0], opportunity[2])
                for opportunity in data
            ]
        }

    abort(500)


@main_blueprint.route("/getProfessorMeta/<string:rcs_id>", methods=["GET"])
def getProfessorMeta(rcs_id: str):
    if request.method == "GET":
        # data = request.json

        # user_id = data["user_id"]
        # auth_token = data["authToken"]

        # query database to match user id and password from data received
        query = db.session.execute(
            db.select(LabManager).filter(LabManager.rcs_id == rcs_id)
        )

        # if match, return user data
        # more fields to be added here later

        data = query.all()[0][0]

        return data.to_dict()

    abort(500)


# _______________________________________________________________________________________________#

# Editing Opportunities in Profile Page


@main_blueprint.route("/getOpportunityMeta/<int:id>", methods=["GET"])
def getOpportunityMeta(id: int):
    if request.method == "GET":
        query = db.session.execute(
            db.select(
                Opportunities, RecommendsMajors, RecommendsCourses, RecommendsClassYears
            )
            .filter(Opportunities.id == id)
            .join(RecommendsMajors, RecommendsMajors.opportunity_id == Opportunities.id)
            .join(
                RecommendsCourses, RecommendsCourses.opportunity_id == Opportunities.id
            )
            .join(
                RecommendsClassYears,
                RecommendsClassYears.opportunity_id == Opportunities.id,
            )
        )
        data = query.all()

        if not data or len(data) == 0:
            abort(404)

        data = data[0]

        print(data)

        dictionary = data[0].to_dict()
        dictionary["courses"] = [data[2].course_code]
        dictionary["majors"] = [data[1].major_code]
        dictionary["years"] = [data[3].class_year]

        return {"data": dictionary}

    abort(500)


@main_blueprint.route("/deleteOpportunity", methods=["DELETE", "POST"])
def deleteOpportunity():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        postID = data["postID"]
        authToken = data["authToken"]
        authorID = data["authorID"]

        query = db.session.execute(
            db.select(Leads, Opportunities)
            .filter(Leads.opportunity_id == postID)
            .filter(Leads.lab_manager_rcs_id == authorID)
            .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        )

        data = query.all()

        # query database to see if the credentials above match
        print("pritning data")
        data = data[0][0]

        # data.delete()
        # if match is found, delete the opportunity, return status 200

        return {"name": "Done"}

    abort(500)


@main_blueprint.route("/changeActiveStatus", methods=["DELETE", "POST"])
def changeActiveStatus():
    if request.method in ["POST"]:
        data = request.json
        postID = data["oppID"]
        authToken = data["authToken"]
        setStatus = data["setStatus"]

        # query database to see if the credentials above match
        query = db.session.execute(
            db.select(Opportunities)
            .filter(Opportunities.id == postID)
        )

        data = query.all()
        print(data)

        if not data or len(data) == 0:
            abort(404)

        data = data[0][0]

        data.active = setStatus
        
        db.session.commit()
        
        if data.active != setStatus:
            abort(500)

        # if match is found, change the opportunities active status to true or false based on setStatus

        return {"activeStatus": data.active}

    abort(500)


@main_blueprint.route("/editOpportunity", methods=["DELETE", "POST"])
def editOpportunity():
    if request.method in ["POST"]:
        data = request.json
        postID = data["postID"]
        authToken = data["authToken"]
        authorID = data["authorID"]
        newPostData = data["newPostData"]

        # query database to see if the credentials above match
        query = db.session.execute(
            db.select(Leads, Opportunities)
            .filter(Leads.opportunity_id == postID)
            .filter(Leads.lab_manager_rcs_id == authorID)
            .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        )

        data = query.all()[0][0]

        # if match is found, edit the opportunity with the new data provided
        data.name = newPostData["name"]
        data.description = newPostData["description"]
        data.recommended_experience = newPostData["recommended_experience"]
        data.pay = newPostData["pay"]
        data.credits = newPostData["credits"]
        data.semester = newPostData["semester"]
        data.year = newPostData["year"]
        data.application_due = newPostData["application_due"]
        data.active = newPostData["active"]

        abort(200)

    abort(500)


# create fake opportunity
"""
{
    "authorID": "led",
    "newPostData": {
        "name": "Abid's AC System",
        "description": "Time to cool your room with a new AC system!",
        "recommended_experience": "Computer Science, ITWS, or any other major with a focus on technology.",
        "pay": 25.0,
        "credits": "4",
        "semester": "Fall",
        "year": 2024,
        "application_due": "2024-03-30",
        "active": True,
        "courses": ["CSCI4430"],
        "majors": ["PHYS"],
        "years": [2023, 2024]
    }
}

"""


@main_blueprint.route("/createOpportunity", methods=["POST"])
def createOpportunity():
    if request.method == "POST":
        data = request.json
        authorID = data["authorID"]
        newPostData = data["newPostData"]

        # query database to see if the credentials above match
        query = db.session.execute(
            db.select(LabManager).filter(LabManager.rcs_id == authorID)
        )

        data = query.all()[0][0]

        # TODO: how do we get the opportunity id?
        # if match is found, create a new opportunity with the new data provided
        newOpportunity = Opportunities(
            name=newPostData["name"],
            description=newPostData["description"],
            recommended_experience=newPostData["recommended_experience"],
            pay=newPostData["pay"],
            credits=newPostData["credits"],
            semester=newPostData["semester"],
            year=newPostData["year"],
            application_due=datetime.datetime.strptime(
                newPostData["application_due"], "%Y-%m-%d"
            ),
            active=newPostData["active"],
        )
        db.session.add(newOpportunity)
        db.session.commit()

        newLead = Leads(lab_manager_rcs_id=authorID, opportunity_id=newOpportunity.id)

        db.session.add(newLead)
        db.session.commit()

        for course in newPostData["courses"]:
            newCourse = RecommendsCourses(
                opportunity_id=newOpportunity.id, course_code=course
            )
            db.session.add(newCourse)
            db.session.commit()

        for major in newPostData["majors"]:
            newMajor = RecommendsMajors(
                opportunity_id=newOpportunity.id, major_code=major
            )
            db.session.add(newMajor)
            db.session.commit()

        for year in newPostData["years"]:
            newYear = RecommendsClassYears(
                opportunity_id=newOpportunity.id, class_year=year
            )
            db.session.add(newYear)
            db.session.commit()

        # db.session.add(newOpportunity)

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
