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


@main_blueprint.route("/")
def index():
    return {"Hello": "There"}


@main_blueprint.route("/opportunities")
def positions():
    return {"Hello": "There"}


@main_blueprint.get("/profile")
def profile():
    request_data = request.get_json()
    rcs_id = request_data.get("rcs_id", None)

    lab_manager = db.first_or_404(
        db.select(LabManager).filter(LabManager.rcs_id == rcs_id)
    )

    result = lab_manager.to_dict()

    data = db.session.execute(
        db.select(Opportunities, Leads)
        .filter(Leads.lab_manager_rcs_id == rcs_id)
        .join(Opportunities, Leads.opportunity_id == Opportunities.id)
    ).scalars()

    result["opportunities"] = [opportunity.to_dict() for opportunity in data]

    return result


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
        for item in data:
            if item[0].name not in dictionary:
                dictionary[item[0].name] = []
            dictionary[item[0].name].append(item[1].name)

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
