from flask import abort, render_template

from . import main_blueprint
from labconnect import db
from labconnect.models import (
    RPIDepartments,
    ContactLinks,
    LabRunner,
    Opportunities,
    Courses,
    Majors,
    ClassYears,
    ApplicationDueDates,
    Semesters,
    SalaryCompInfo,
    UpfrontPayCompInfo,
    CreditCompInfo,
    IsPartOf,
    HasLink,
    Promotes,
    RecommendsCourses,
    RecommendsMajors,
    RecommendsClassYears,
    ApplicationDue,
    ActiveSemesters,
    HasSalaryComp,
    HasUpfrontPayComp,
    HasCreditComp,
)

@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/opportunities")
def positions():
    # pass objects into render_template. For example:
    # lines = ...
    # return render_template("opportunitys.html", lines=lines)

    # https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query
    

    inst = db.inspect(Opportunities)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    print("all attributes in order:", attr_names)

    attr_names = attr_names[1:]

    """
    query = db.session.query(
        # Opportunities.opp_id, 
        Opportunities.name,
        Opportunities.description,
        Opportunities.active_status,
        Opportunities.recommended_experience
    )
 
    # executing the query with db
    result = query.all()
    rows = [",".join(str(row).split(",")) for row in result]
    print(rows)
    """
    stmt = db.select(
        # Opportunities.opp_id, 
        Opportunities.name,
        LabRunner.name
    ).join(
        Promotes, Opportunities.opp_id == Promotes.opportunity_id
    ).join(
        LabRunner, Promotes.lab_runner_rcs_id == LabRunner.rcs_id
    )
    print(stmt)

    result = db.session.execute(stmt)
    print(result)

    rows = list()
    for row in result.scalars():
        print(row)
        rows.append(row)

    return render_template(
        "opportunitys.html", 
        attr_names = attr_names, 
        opp_attr_rows = rows
    )


@main_blueprint.route("/opportunity/<int:id>")
def opportunity(id: int):
    return render_template("opportunity_details.html")


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return render_template("profile.html")


@main_blueprint.route("/department/<string:department>")
def department(department: str):
    return render_template("department.html")


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
