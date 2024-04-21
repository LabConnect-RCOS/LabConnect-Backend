import datetime
from typing import Any

from flask import abort, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)

from labconnect import bcrypt, db
from labconnect.models import (
    ClassYears,
    Courses,
    LabManager,
    Leads,
    Majors,
    Opportunities,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
    User,
    UserCourses,
    UserDepartments,
    UserMajors,
    Participates,
    RecommendsCourses,
    RecommendsClassYears,
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

    credits = ""
    if opportunityInfo.one_credit:
        credits += "1, "
    if opportunityInfo.two_credits:
        credits += "2, "
    if opportunityInfo.three_credits:
        credits += "3, "
    if opportunityInfo.four_credits:
        credits += "4"

    if credits != "":
        credits += " credits"

    data["aboutSection"] = [
        {
            "title": "Pay",
            "description": f"${opportunityInfo.pay} per hour",
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

    if credits != "":
        data["aboutSection"].append(
            {
                "title": "Credits",
                "description": credits,
            }
        )

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


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return {"Hello": "There"}


@main_blueprint.route("/department")
def department():

    if not request.data:
        abort(400)

    json_request_data = request.get_json()

    if not json_request_data:
        abort(400)

    department = json_request_data.get("department", None)

    if not department:
        abort(400)

    department_data = db.first_or_404(
        db.select(RPIDepartments).where(RPIDepartments.name == department)
    )

    result = department_data.to_dict()

    prof_data = db.session.execute(
        db.select(LabManager).where(LabManager.department_id == department)
    ).scalars()

    query = (
        db.select(Opportunities)
        .where(Opportunities.active == True)
        .limit(20)
        .join(Leads, Opportunities.id == Leads.opportunity_id)
        .join(LabManager, Leads.lab_manager_rcs_id == LabManager.rcs_id)
        .distinct()
    )

    professors = []
    where_conditions = []

    for prof in prof_data:
        professors.append({"name": prof.name, "rcs_id": prof.rcs_id})
        where_conditions.append(LabManager.rcs_id == prof.rcs_id)

    result["professors"] = professors

    query = query.where(db.or_(*where_conditions))
    data = db.session.execute(query).scalars()
    opportunities = [opportunity.to_dict() for opportunity in data]

    result["opportunities"] = opportunities

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
            db.select(RPISchools, RPIDepartments).join(
                RPIDepartments, RPISchools.name == RPIDepartments.school_id
            )
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

    json_request_data = request.get_json()

    if not json_request_data:
        abort(400)

    rcs_id = json_request_data.get("rcs_id", None)

    if not rcs_id:
        abort(400)

    data = db.first_or_404(db.select(LabManager).where(LabManager.rcs_id == rcs_id))

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
    dictionary["image"] = (
        "https://cdn.dribbble.com/users/2033319/screenshots/12591684/media/0557608c87ed8c5a80bd5faa48c3cd71.png"
    )
    dictionary["department"] = data.department_id
    dictionary["email"] = data.rcs_id + "@rpi.edu"
    dictionary["role"] = "admin"
    dictionary["description"] = (
        "I am the evil professor Doofenshmirtz. I am a professor at RPI and I am looking for students to help me with my evil schemes"
    )
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

    data = db.session.execute(
        db.select(Opportunities, LabManager)
        .filter(LabManager.rcs_id == rcs_id)
        .join(Leads, LabManager.rcs_id == Leads.lab_manager_rcs_id)
        .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        .order_by(Opportunities.id)
    ).scalars()

    if not data:
        abort(404)

    result = {rcs_id: [opportunity.to_dict() for opportunity in data]}

    return result


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

            if (
                opportunity.one_credit
                or opportunity.two_credits
                or opportunity.three_credits
                or opportunity.four_credits
            ):
                oppData["attributes"].append("Credit Available")

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
            if (
                opportunity.one_credit
                or opportunity.two_credits
                or opportunity.three_credits
                or opportunity.four_credits
            ):
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


# _______________________________________________________________________________________________#


# Editing Opportunities in Profile Page
@main_blueprint.route("/getProfessorCookies/<string:id>", methods=["GET"])
def getProfessorCookies(id: str):
    # this is already restricted to "GET" requests

    query = db.session.execute(db.select(LabManager).filter(LabManager.rcs_id == id))

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

        dictionary["credits"] = []
        if dictionary["one_credit"]:
            dictionary["credits"].append("1")

        if dictionary["two_credits"]:
            dictionary["credits"].append("2")

        if dictionary["three_credits"]:
            dictionary["credits"].append("3")

        if dictionary["four_credits"]:
            dictionary["credits"].append("4")

        dictionary.pop("one_credit")
        dictionary.pop("two_credits")
        dictionary.pop("three_credits")
        dictionary.pop("four_credits")

        return {"data": dictionary}

    abort(500)


@main_blueprint.route("/deleteOpportunity", methods=["DELETE", "POST"])
def deleteOpportunity():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        id = data["id"]

        query = db.session.execute(
            db.select(
                Opportunities,
                RecommendsMajors,
                RecommendsCourses,
                RecommendsClassYears,
                Leads,
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

        one = False
        two = False
        three = False
        four = False

        if "1" in newPostData["credits"]:
            one = True
        if "2" in newPostData["credits"]:
            two = True
        if "3" in newPostData["credits"]:
            three = True
        if "4" in newPostData["credits"]:
            four = True

        # if match is found, edit the opportunity with the new data provided
        opportunity.name = newPostData["name"]
        opportunity.description = newPostData["description"]
        opportunity.recommended_experience = newPostData["recommended_experience"]
        opportunity.pay = newPostData["pay"]
        opportunity.one_credit = one
        opportunity.two_credits = two
        opportunity.three_credits = three
        opportunity.four_credits = four
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
            newMajor = RecommendsMajors(opportunity_id=opportunity.id, major_code=major)
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

        one = False
        two = False
        three = False
        four = False

        if "1" in newPostData["credits"]:
            one = True
        if "2" in newPostData["credits"]:
            two = True
        if "3" in newPostData["credits"]:
            three = True
        if "4" in newPostData["credits"]:
            four = True

        newOpportunity = Opportunities(
            name=newPostData["name"],
            description=newPostData["description"],
            recommended_experience=newPostData["recommended_experience"],
            pay=newPostData["pay"],
            one_credit=one,
            two_credits=two,
            three_credits=three,
            four_credits=four,
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

        print("got here atleast")

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

    json_request_data = request.get_json()

    if not json_request_data:
        abort(400)

    email = json_request_data.get("email", None)
    password = json_request_data.get("password", None)
    first_name = json_request_data.get("first_name", None)
    last_name = json_request_data.get("last_name", None)
    class_year = json_request_data.get("class_year", None)

    if (
        email is None
        or password is None
        or first_name is None
        or last_name is None
        or class_year is None
        or not isinstance(email, str)
        or not isinstance(password, str)
        or not isinstance(first_name, str)
        or not isinstance(last_name, str)
        or not isinstance(class_year, int)
    ):
        abort(400)

    data = db.session.execute(db.select(User).where(User.email == email)).scalar()

    if data is None:

        user = User(
            email=email,
            password=bcrypt.generate_password_hash(password + email),
            first_name=first_name,
            last_name=last_name,
            preferred_name=json_request_data.get("preferred_name", None),
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

    json_request_data = request.get_json()

    if not json_request_data:
        abort(400)

    email = json_request_data.get("email", None)
    password = json_request_data.get("password", None)

    if email is None or password is None:
        abort(400)

    data = db.session.execute(db.select(User).where(User.email == email)).scalar()

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

        json_request_data = request.get_json()

        if not json_request_data:
            abort(400)

        partial_key = json_request_data.get("input", None)

        data = db.session.execute(
            db.select(Majors)
            .order_by(Majors.code)
            .where(
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
        .where(ClassYears.active == True)
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

    result = [course.to_dict() for course in data]

    if result == []:
        abort(404)

    return result


@main_blueprint.get("/user")
def user():
    if not request.data:
        abort(400)

    id = request.get_json().get("id", None)

    if not id:
        abort(400)

    # Query for user
    user = db.first_or_404(db.select(User).filter(User.id == id))
    result = user.to_dict()

    # Query for user's department(s)
    user_departments = db.session.execute(
        db.select(UserDepartments).filter(UserDepartments.user_id == id)
    ).scalars()
    result["departments"] = [dept.to_dict() for dept in user_departments]

    # Query for user's major(s)
    user_majors = db.session.execute(
        db.select(UserMajors).filter(UserMajors.user_id == id)
    ).scalars()
    result["majors"] = [major.to_dict() for major in user_majors]

    # Query for user's courses
    user_courses = db.session.execute(
        db.select(UserCourses)
        .order_by(UserCourses.in_progress)
        .filter(UserCourses.user_id == id)
    ).scalars()
    result["courses"] = [course.to_dict() for course in user_courses]

    # Query for user's opportunities
    user_opportunities = db.session.execute(
        db.select(Opportunities, Participates)
        .filter(Participates.user_id == id)
        .join(Opportunities, Participates.opportunity_id == Opportunities.id)
        .order_by(Opportunities.active.desc())
    ).scalars()
    result["opportunities"] = [
        opportunity.to_dict() for opportunity in user_opportunities
    ]

    return result
