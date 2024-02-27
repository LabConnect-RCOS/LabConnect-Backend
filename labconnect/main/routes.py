from flask import abort, render_template, request

from labconnect import db
from labconnect.helpers import SemesterEnum
from labconnect.models import (
    Opportunities,
    RPIDepartments,
    RPISchools,
    LabManager,
    Leads,
)

from . import main_blueprint


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/opportunities")
def positions():
    return "Hello There"


@main_blueprint.route("/opportunity/<int:id>")
def opportunity(id: int):
    return "General Kenobi"


@main_blueprint.route("/profile")
def profile():
    request_data = request.get_json()

    rcs_id = request_data.get("Profile", {}).get("rcs_id", None)
    name = request_data.get("Profile", {}).get("name", None)
    email = request_data.get("Profile", {}).get("email", None)
    phone_number = request_data.get("Profile", {}).get("phone_number", None)
    website = request_data.get("Profile", {}).get("website", None)
    title = request_data.get("Profile", {}).get("title", None)
    department = request_data.get("Profile", {}).get("department", None)
    # past_opportunities = request_data.get('Profile', {})['past_opportunities']
    # currrent_opportunities = request_data.get('Profile', {})['currrent_opportunities']

    return {
        "Profile": {
            "rcs_id": rcs_id,
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "website": website,
            "title": title,
            "departments": department,
            "past_opportunities": [
                {
                    "professor": "Kuzman",
                    "credits": 4,
                    "description": "RCOS",
                }
            ],
            "current_opportunities": [
                {"professor": "Xiao", "credits": 4, "description": "DataStructures"}
            ],
        }
    }


@main_blueprint.route("/department")
def department():
    data_query = (
        db.session.query(
            RPIDepartments.name, RPIDepartments.description, RPISchools.name
        )
        .filter(RPIDepartments.name == "Computer Science")
        .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
    ).first()
    # data = data_query.all()
    print(data)

    professors = (
        db.session.query(
            # Need all professors
            RPIDepartments.name
        )
        # Professors department needs to match department (data[0])
        .filter(RPIDepartments.name == data[0])
        # .join(RPISchools, RPIDepartments.school_id == RPISchools.name)
    ).first()

    # rpidepartment.name

    return {"department": data[0], "description": data[1], "school": data[2]}


@main_blueprint.route("/discover")
def discover():
    return render_template("discover.html")


@main_blueprint.route("/professor/<string:rcs_id>")
def professor(rcs_id: str):
    # test code until database code is added
    if "bob" == rcs_id:
        return render_template("professor.html")
    abort(500)


@main_blueprint.route("/create_post")
def create_post():
    return render_template("posting.html")


@main_blueprint.route("/login")
def login():
    return render_template("sign_in.html")


@main_blueprint.route("/information")
@main_blueprint.route("/info")
def information():
    return render_template("URP_Basic_Information_Page.html")


@main_blueprint.route("/tips")
def tips():
    return render_template("tips_and_tricks.html")
