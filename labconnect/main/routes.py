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


@main_blueprint.route("/")
def index():
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

    # print(result)

    # Might not need
    if not request.data:
        abort(400)

    professors = request.get_json().get("department", None)

    if not professors:
        abort(400)

    # departmentOf department_name
    prof_data = db.session.execute(
        db.select(LabManager.name).filter(LabManager.department_id == department)
        # RPIDepartments.name == result[0]
        # .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
        .join(
            # Need =
            RPIDepartments,
            LabManager.department_id == RPIDepartments.name,
        )
        # LabManager.rcs_id,
        # LabManager.name,
        # LabManager.department_id,
        # )
        # rcs_id=row_tuple[0], name=row_tuple[1], department_id=row_tuple[2]
        # , RPIDepartments.school_id == RPISchools.name)
    ).scalars()
    # print(department)
    # for prof in prof_data:
    # print(prof)
    # prof.to_dict()

    # print(prof_data)
    # result2 = prof_data
    # result2 = prof_data.todict()
    # result2 = [prof_data.to_dict() for prof_data in data]
    print(type(prof_data))
    result2 = prof_data
    # result2 = [prof.to_dict() for prof in prof_data]
    # rcs_id=row_tuple[0], name=row_tuple[1], department_id=row_tuple[2]
    # return result2?

    return result2


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
