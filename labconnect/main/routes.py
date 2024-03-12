from flask import abort, render_template, request

from labconnect import db
from labconnect.helpers import SemesterEnum
from labconnect.models import Opportunities, RPIDepartments, RPISchools

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


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return render_template("profile.html")


@main_blueprint.route("/department")
def department():
    # return {"professors": ["Turner", "Kuzmin"], "projects": ["project1", "project2"]}
    # department = request.args.get(department)
    # @app.route('/json-example', methods=['POST'])
    request_data = request.get_json()
    # language = request_data["department"]
    department = request_data.get("department", None)

    # departmentOf department_name
    data = (
        db.session.query(
            RPIDepartments.name, RPIDepartments.description, RPISchools.name
        )
        .filter(RPIDepartments.name == department)
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
