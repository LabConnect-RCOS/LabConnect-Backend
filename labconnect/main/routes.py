from flask import abort, render_template, request

from labconnect import db
from labconnect.helpers import SemesterEnum
from labconnect.main.queries import (
    get_opportunity_active_semesters,
    get_opportunity_application_due_dates,
    get_opportunity_course_credits,
    get_opportunity_hourly_rates,
    get_opportunity_promoters,
    get_opportunity_recommended_class_years,
    get_opportunity_recommended_courses,
    get_opportunity_recommended_majors,
    get_opportunity_upfront_pay,
)
from labconnect.models import Opportunities, RPIDepartments, DepartmentOf

from . import main_blueprint


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/opportunities")
def positions():
    return "Hello There"
    # # pass objects into render_template. For example:
    # # lines = ...
    # # return render_template("opportunitys.html", lines=lines)

    # """
    # For each opportunity summary:
    #     name of opportunity,
    #     description,
    #     recommended majors,
    #     lab runners promoting,
    #     all forms of compensation,
    # Return only opportunities active in any given semester
    # """

    # # Requires application logic to update current semester
    # current_semester = (2023, "Fall")

    # TURN_OFF_SEMESTER_FILTER = False
    # active_opp_ids = (
    #     db.session.query(Opportunities.opp_id)
    #     .join(ActiveSemesters, ActiveSemesters.opportunity_id == Opportunities.opp_id)
    #     .filter(
    #         (ActiveSemesters.year == current_semester[0])
    #         & (ActiveSemesters.season == current_semester[1])
    #         | TURN_OFF_SEMESTER_FILTER
    #     )
    #     .order_by(Opportunities.opp_id)
    # )

    # names = (
    #     db.session.query(Opportunities.name)
    #     .join(ActiveSemesters, ActiveSemesters.opportunity_id == Opportunities.opp_id)
    #     .filter(
    #         (ActiveSemesters.year == current_semester[0])
    #         & (ActiveSemesters.season == current_semester[1])
    #         | TURN_OFF_SEMESTER_FILTER
    #     )
    #     .order_by(Opportunities.opp_id)
    # )

    # descriptions = (
    #     db.session.query(Opportunities.description)
    #     .join(ActiveSemesters, ActiveSemesters.opportunity_id == Opportunities.opp_id)
    #     .filter(
    #         (ActiveSemesters.year == current_semester[0])
    #         & (ActiveSemesters.season == current_semester[1])
    #         | TURN_OFF_SEMESTER_FILTER
    #     )
    #     .order_by(Opportunities.opp_id)
    # )

    # majors = list()
    # promoters = list()
    # credits = list()
    # salaries = list()
    # upfront_pay = list()

    # for opp_id in active_opp_ids.all():
    #     # Access via opp_id[0]
    #     majors.append(get_opportunity_recommended_majors(opp_id[0]))
    #     promoters.append(get_opportunity_promoters(opp_id[0]))
    #     credits.append(get_opportunity_course_credits(opp_id[0]))
    #     salaries.append(get_opportunity_hourly_rates(opp_id[0]))
    #     upfront_pay.append(get_opportunity_upfront_pay(opp_id[0]))

    # print(active_opp_ids.all())
    # print(names.all())
    # print(descriptions.all())
    # for eachlist in [majors, promoters, credits, salaries, upfront_pay]:
    #     print("-" * 32)
    #     for each in eachlist:
    #         print(each.all())

    # """
    # result = joined_query1.all()
    # joined_query1_rows = [", ".join(str(row).split(",")) for row in result]
    # """

    # return render_template(
    #     "opportunitys.html",
    #     names=names,
    #     descriptions=descriptions,
    #     majors=majors,
    #     promoters=promoters,
    #     credits=credits,
    #     salaries=salaries,
    #     upfront_pay=upfront_pay,
    # )


@main_blueprint.route("/opportunity/<int:id>")
def opportunity(id: int):
    return "General Kenobi"
    # promoters_attr_names = ["rcs_id", "name"]

    # promoters = get_opportunity_promoters(id).all()

    # # Columns "course_code", "course_name"
    # recommended_courses = get_opportunity_recommended_courses(id).all()

    # # Columns "major_code", "major_name"
    # recommended_majors = get_opportunity_recommended_majors(id).all()

    # # Columns "class_year", "class_name"
    # recommended_class_years = get_opportunity_recommended_class_years(id).all()

    # # Columns "usd_per_hour"
    # salaries = get_opportunity_hourly_rates(id).all()

    # # Columns "usd"
    # upfront_pay = get_opportunity_upfront_pay(id).all()

    # # Columns "course_code", "number_of_credits"
    # course_credits = get_opportunity_course_credits(id).all()

    # # Columns "date"
    # application_due_dates = get_opportunity_application_due_dates(id).all()

    # # Columns "year", "season"
    # active_semesters = get_opportunity_active_semesters(id).all()

    # return render_template(
    #     "opportunity_details.html",
    #     promoters_attr_names=promoters_attr_names,
    #     promoters=promoters,
    #     recommended_courses=recommended_courses,
    #     recommended_majors=recommended_majors,
    #     recommended_class_years=recommended_class_years,
    #     salaries=salaries,
    #     upfront_pay=upfront_pay,
    #     course_credits=course_credits,
    #     application_due_dates=application_due_dates,
    #     active_semesters=active_semesters,
    # )


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return render_template("profile.html")


@main_blueprint.route("/department")
def department():
    # return {"professors": ["Turner", "Kuzmin"], "projects": ["project1", "project2"]}
    #department = request.args.get(department)
    #@app.route('/json-example', methods=['POST'])
    request_data = request.get_json()
    #language = request_data["department"]
    department = request_data.get("department", None)
    data = (
        db.session.query(RPIDepartments.name, RPIDepartments.description)
        .filter(RPIDepartments.name == department)
        .join(DepartmentOf, DepartmentOf.department_name == RPIDepartments.name)
        .all()
    )
    print(data)
    # departmentOf department_name


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
