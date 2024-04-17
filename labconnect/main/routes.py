import datetime


from typing import Any

from flask import abort, jsonify, redirect, request, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)

from labconnect import bcrypt, db
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
    User,
)

from . import main_blueprint


def packageOpportunity(opportunityInfo, professorInfo):
    data = opportunityInfo.to_dict()
    data["professor"] = professorInfo.name
    data["department"] = professorInfo.department_id

    return data



def packageIndividualOpportunity(opportunityInfo, professorInfo):
    data = {}
    data["id"] = opportunityInfo.id
    data["name"] = opportunityInfo.name
    data["description"] = opportunityInfo.description
    data["recommended_experience"] = opportunityInfo.recommended_experience
    data["author"] = professorInfo.name
    data["department"] = professorInfo.department_id

    data["aboutSection"] = [
        {
            "title": "Pay",
            "description": f"${opportunityInfo.pay} per hour",
        },
        {
            "title": "Credits",
            "description": f"{opportunityInfo.credits} credits",
        },
        {
            "title": "Semester",
            "description": f"{opportunityInfo.semester} {opportunityInfo.year}",
        },
        {
            "title": "Application Due",
            "description": opportunityInfo.application_due,
        },
    ]

    return data


def packageOpportunityCard(opportunity):

    # get professor and department by getting Leads and LabManager
    query = db.session.execute(
        db.select(Leads, LabManager)
        .filter(Leads.opportunity_id == opportunity.id)
        .join(LabManager, Leads.lab_manager_rcs_id == LabManager.rcs_id)
    )

    data = query.all()

    professor = data[0][1]

    card = {
        "id": opportunity.id,
        "title": opportunity.name,
        "professor": professor.name,
        "season": opportunity.semester,
        "location": "TBA",
        "year": opportunity.year,
    }

    return card

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
    query = (
        # db.session.query(Opportunities, Majors)
        # .filter(Majors.major_code == "CSCI")
        # .join(RecommendsMajors, Majors.major_code == RecommendsMajors.major_code)
        # .join(Opportunities, Opportunities.id == RecommendsMajors.opportunity_id)
        db.select(
            Opportunities.id,
            Opportunities.name,
            Opportunities.description,
            Opportunities.pay,
            Majors,
            RecommendsMajors,
        )
        .filter(Majors.code == "CSCI")
        .join(Opportunities, Opportunities.id == RecommendsMajors.opportunity_id)
        .join(Majors, RecommendsMajors.major_code == Majors.code)
        # commented out code above needs fixing
    )

    print(query)
    return {
        "data": [
            {
                "title": "Nelson",
                "major": "CS",
                # "experience": "x",
                # "description": "d",
                "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
                "credits": 4,
                "pay": 9000.0,
            },
            {
                "title": "Name",
                "major": "Major",
                # "experience": "XP",
                # "description": "Hi",
                "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
                "credits": 3,
                "pay": 123,
            },
        ]
    }

@main_blueprint.route("/getSchoolsAndDepartments/", methods=["GET"])
def getSchoolsAndDepartments():
    if request.method == "GET":
        query = db.session.execute(
            db.select(RPISchools, RPIDepartments)
            .join(RPIDepartments, RPISchools.name == RPIDepartments.school_id)
        )
        data = query.all()

        dictionary = {}
        for tuple in data:
            if tuple[0].name not in dictionary:
                dictionary[tuple[0].name] = []
            dictionary[tuple[0].name].append(tuple[1].name)

        return dictionary
    abort(400)

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

@main_blueprint.get("/lab_manager")
def getLabManagers():
    if not request.data:
        abort(400)

    rcs_id = request.get_json().get("rcs_id", None)

    if not rcs_id:
        abort(400)

    data = db.first_or_404(db.select(LabManager).filter(LabManager.rcs_id == rcs_id))

    result = data.to_dict()

    return result


@main_blueprint.route("/getProfessorProfile/<string:rcs_id>", methods=["GET"])
def getProfessorProfile(rcs_id: str):
    # test code until database code is added
    query = db.session.execute(
        db.select(LabManager).filter(LabManager.rcs_id == rcs_id)
    )

    data = query.all()
    data = data[0][0]
    dictionary = data.to_dict()
    dictionary.pop("rcs_id")
    dictionary["image"] = "https://cdn.dribbble.com/users/2033319/screenshots/12591684/media/0557608c87ed8c5a80bd5faa48c3cd71.png"
    dictionary["department"] = data.department_id
    dictionary["email"] = data.rcs_id + "@rpi.edu"
    dictionary["role"] = "admin"
    dictionary["description"] = "I am the evil professor Doofenshmirtz. I am a professor at RPI and I am looking for students to help me with my evil schemes"
    dictionary["phone"] = "123-456-7890"
    return dictionary




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

    oppData = packageIndividualOpportunity(data[0], data[2])

    # return data in the below format if opportunity is found
    return {"data": oppData}


@main_blueprint.get("/lab_manager/opportunities")
def getLabManagerOpportunityCards() -> dict[Any, list[Any]]:
    if not request.data:
        abort(400)

    rcs_id = request.get_json().get("rcs_id", None)

    if not rcs_id:
        abort(400)

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

            if opportunity.pay != None and opportunity.pay > 0:
                oppData["attributes"].append("Paid")

            if opportunity.credits != None:
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

            oppData = {
                "id": opportunity.id,
                "title": opportunity.name,
                "body": "Due " + str(opportunity.application_due),
                "attributes": [],
                "activeStatus": opportunity.active,
            }

            if opportunity.pay != None and opportunity.pay > 0:
                oppData["attributes"].append("Paid")
            if opportunity.credits != None and ("1" in opportunity.credits or "2" in opportunity.credits or "3" in opportunity.credits or "4" in opportunity.credits):
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

# Jobs page

@main_blueprint.route("/getOpportunityCards", methods=["GET"])
def getOpportunityCards():
    if request.method == "GET":
        # query database for opportunity
        query = db.session.execute(
            db.select(Opportunities, Leads)
            .filter(Opportunities.active == True)
            .join(Leads, Leads.opportunity_id == Opportunities.id)
        )

        data = query.fetchall()

        # return data in the below format if opportunity is found
        return {
            "data": [packageOpportunityCard(opportunity[0]) for opportunity in data]
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
@main_blueprint.route("/getProfessorCookies/<string:id>", methods=["GET"])
def getProfessorCookies(id: str):
    # this is already restricted to "GET" requests

    query = db.session.execute(
        db.select(LabManager).filter(LabManager.rcs_id == id)
    )

    data = query.all()
    data = data[0][0]
    # print(data)
    dictionary = data.to_dict()
    dictionary["id"] = data.rcs_id
    dictionary["department"] = data.department_id
    dictionary["role"] = "admin"
    dictionary["researchCenter"] = "AI"
    dictionary["loggedIn"] = True

    # remove rcs_id from dictionary
    dictionary.pop("rcs_id")

    return dictionary

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
        print(data)

        if not data or len(data) == 0:
            abort(404)

        dictionary = data[0][0].to_dict()
        dictionary["semester"] = dictionary["semester"].upper()
        dictionary["courses"] = set()
        dictionary["majors"] = set()
        dictionary["years"] = set()

        for row in data:
                dictionary["courses"].add(row[2].course_code)
                dictionary["majors"].add(row[1].major_code)
                dictionary["years"].add(row[3].class_year)

        dictionary["courses"] = list(dictionary["courses"])
        dictionary["majors"] = list(dictionary["majors"])
        dictionary["years"] = list(dictionary["years"])

        for i in range(len(dictionary["years"])):
            dictionary["years"][i] = str(dictionary["years"][i])

        return {"data": dictionary}

    abort(500)


@main_blueprint.route("/deleteOpportunity", methods=["DELETE", "POST"])
def deleteOpportunity():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        id = data["id"]

        query = db.session.execute(
            db.select(
                Opportunities, RecommendsMajors, RecommendsCourses, RecommendsClassYears, Leads
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
            .join(Leads, Leads.opportunity_id == Opportunities.id)
        )

        data = query.all()
        print(data)

        if not data or len(data) == 0:
            abort(404)

        opportunity = data[0][0]

        for row in data:
            db.session.delete(row[1])
            db.session.delete(row[2])
            db.session.delete(row[3])
            db.session.delete(row[4])

        leads = data[0][4]

        db.session.delete(opportunity)


        db.session.commit()

        return "Success"

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
            db.select(Opportunities).filter(Opportunities.id == postID)
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
    if True:
        data = request.json
        id = data["id"]
        # authToken = data["authToken"]
        # authorID = data["authorID"]
        newPostData = data

        # query database to see if the credentials above match
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

        opportunity = data[0][0]

        # if match is found, edit the opportunity with the new data provided
        opportunity.name = newPostData["name"]
        opportunity.description = newPostData["description"]
        opportunity.recommended_experience = newPostData["recommended_experience"]
        opportunity.pay = newPostData["pay"]
        opportunity.credits = newPostData["credits"]
        opportunity.semester = newPostData["semester"]
        opportunity.year = newPostData["year"]
        opportunity.application_due = datetime.datetime.strptime(
            newPostData["application_due"], "%Y-%m-%d"
        )
        opportunity.active = newPostData["active"]
        db.session.add(opportunity)
        db.session.commit()

        # delete all the old data in the recommends tables

        for row in data:
            db.session.delete(row[1])
            db.session.delete(row[2])
            db.session.delete(row[3])

        # create new data for allow the tables

        for course in newPostData["courses"]:
            newCourse = RecommendsCourses(
                opportunity_id=opportunity.id, course_code=course
            )
            db.session.add(newCourse)
            db.session.commit()

        for major in newPostData["majors"]:
            newMajor = RecommendsMajors(
                opportunity_id=opportunity.id, major_code=major
            )
            db.session.add(newMajor)
            db.session.commit()

        for year in newPostData["years"]:
            newYear = RecommendsClassYears(
                opportunity_id=opportunity.id, class_year=year
            )
            db.session.add(newYear)
            db.session.commit()

        return "Successful"

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
        newPostData = data

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
        print("before comitting")
        db.session.add(newOpportunity)
        db.session.commit()

        print ("got here atleast")

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

        return {"data": "Opportunity Created"}

    abort(500)


@main_blueprint.route("/create_post", methods=["POST"])
def create_post():
    return {"Hello": "There"}


@main_blueprint.post("/register")
def register():

    if not request.data:
        abort(400)

    json_data = request.get_json()
    email = json_data.get("email", None)
    password = json_data.get("password", None)
    first_name = json_data.get("first_name", None)
    last_name = json_data.get("last_name", None)
    class_year = json_data.get("class_year", None)

    if (
        email is None
        or password is None
        or first_name is None
        or last_name is None
        or class_year is None
    ):
        abort(400)

    data = db.session.execute(db.select(User).filter(User.email == email)).scalar()

    if data is None:
        user = User(
            email=email,
            password=bcrypt.generate_password_hash(password + email),
            first_name=first_name,
            last_name=last_name,
            preferred_name=json_data.get("preferred_name", None),
            class_year=class_year,
        )
        db.session.add(user)
        db.session.commit()

        return {"msg": "User created successfully"}

    return {"msg": "User already exists"}, 403


@main_blueprint.post("/login")
def login():
    if not request.data:
        abort(400)

    json_data = request.get_json()
    email = json_data.get("email", None)
    password = json_data.get("password", None)

    if email is None or password is None:
        abort(400)

    data = db.session.execute(db.select(User).filter(User.email == email)).scalar()

    if data is None:
        abort(401)

    if not bcrypt.check_password_hash(data.password, password + email):
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token": access_token}

    return response


@main_blueprint.get("/logout")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@main_blueprint.route("/500")
def force_error():
    abort(500)


@main_blueprint.get("/schools")
def schools() -> list[Any]:

    data = db.session.execute(db.select(RPISchools).order_by(RPISchools.name)).scalars()

    if not data:
        abort(404)

    result = [school.to_dict() for school in data]

    return result


@main_blueprint.get("/departments")
def departments() -> list[Any]:

    data = db.session.execute(
        db.select(RPIDepartments).order_by(RPIDepartments.name)
    ).scalars()

    if not data:
        abort(404)

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

        if not data:
            abort(404)

        result = [major.to_dict() for major in data]

        return result

    data = db.session.execute(db.select(Majors).order_by(Majors.code)).scalars()

    if not data:
        abort(404)

    result = [major.to_dict() for major in data]

    return result


@main_blueprint.get("/years")
def years() -> list[Any]:

    data = db.session.execute(
        db.select(ClassYears)
        .order_by(ClassYears.class_year)
        .filter(ClassYears.active == True)
    ).scalars()

    if not data:
        abort(404)

    result = [year.class_year for year in data]

    if result == []:
        abort(404)

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

    if not data:
        abort(404)

    result = [course.to_dict() for course in data]

    if result == []:
        abort(404)

    return result
