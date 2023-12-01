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

# https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query


def get_opportunities_rows():
    """
    @RETURNS: a Query to all rows of the opportunites table, for all attributes.
    """
    return db.session.query(
        Opportunities.opp_id,
        Opportunities.name,
        Opportunities.description,
        Opportunities.active_status,
        Opportunities.recommended_experience,
    )


def get_opp_ids():
    """ @RETURNS: a Query to all rows of the opportunities table, containing only opp_ids """
    return db.session.query(Opportunities.opp_id)


def get_opportunity_promoters(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the lab_runner table for all attributes, representing:
        everything about lab runners that promote the opportunity
    """
    return (
        db.session.query(LabRunner.rcs_id, LabRunner.name)
        .join(Promotes, Promotes.lab_runner_rcs_id == LabRunner.rcs_id)
        .join(Opportunities, Opportunities.opp_id == Promotes.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(LabRunner.name)
    )


def get_opportunity_recommended_courses(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the courses table for all attributes, representing:
        everything about courses recommended by the opportunity
    """
    return (
        db.session.query(Courses.course_code, Courses.course_name)
        .join(RecommendsCourses, RecommendsCourses.course_code == Courses.course_code)
        .join(Opportunities, Opportunities.opp_id == RecommendsCourses.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(Courses.course_name)
    )
    pass


def get_opportunity_recommended_majors(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the majors table for all attributes, representing:
        everything about majors recommended by the opportunity
    """
    return (
        db.session.query(Majors.major_code, Majors.major_name)
        .join(RecommendsMajors, RecommendsMajors.major_code == Majors.major_code)
        .join(Opportunities, Opportunities.opp_id == RecommendsMajors.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(Majors.major_name)
    )
    pass


def get_opportunity_recommended_class_years(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the class_years table for all attributes, representing:
        everything about class years recommended by the opportunity
    """
    return (
        db.session.query(ClassYears.class_year, ClassYears.class_name)
        .join(
            RecommendsClassYears,
            RecommendsClassYears.class_year == ClassYears.class_year,
        )
        .join(
            Opportunities, Opportunities.opp_id == RecommendsClassYears.opportunity_id
        )
        .filter(Opportunities.opp_id == opp_id)
        .order_by(ClassYears.class_year)
    )
    pass


def get_opportunity_hourly_rates(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the salary_comp_info table for all attributes, representing:
        everything about hourly salary of the opportunity
    """
    return (
        db.session.query(SalaryCompInfo.usd_per_hour)
        .join(HasSalaryComp, HasSalaryComp.usd_per_hour == SalaryCompInfo.usd_per_hour)
        .join(Opportunities, Opportunities.opp_id == HasSalaryComp.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(SalaryCompInfo.usd_per_hour)
    )
    pass


def get_opportunity_upfront_pay(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the upfront_pay_comp_info table for all attributes, representing:
        everything about upfront pay of the opportunity
    """
    return (
        db.session.query(UpfrontPayCompInfo.usd)
        .join(HasUpfrontPayComp, HasUpfrontPayComp.usd == UpfrontPayCompInfo.usd)
        .join(Opportunities, Opportunities.opp_id == HasUpfrontPayComp.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(UpfrontPayCompInfo.usd)
    )
    pass


def get_opportunity_course_credits(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the credit_comp_info table for all attributes, representing:
        everything about which courses are credited, and range of credits awarded by the opportunity
    """
    return (
        db.session.query(CreditCompInfo.course_code, CreditCompInfo.number_of_credits)
        .join(
            HasCreditComp,
            (HasCreditComp.course_code == CreditCompInfo.course_code)
            & (HasCreditComp.number_of_credits == CreditCompInfo.number_of_credits),
        )
        .join(Opportunities, Opportunities.opp_id == HasCreditComp.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(CreditCompInfo.number_of_credits)
    )
    pass


def get_opportunity_application_due_dates(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the application_due_dates table for all attributes, representing:
        everything about the opportunity's application due dates
    """
    return (
        db.session.query(ApplicationDueDates.date)
        .join(ApplicationDue, ApplicationDue.date == ApplicationDueDates.date)
        .join(Opportunities, Opportunities.opp_id == ApplicationDue.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(ApplicationDueDates.date)
    )
    pass


def get_opportunity_active_semesters(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the semesters table for all attributes, representing:
        everything about the opportunity's active semesters
    """
    return (
        db.session.query(Semesters.year, Semesters.season)
        .join(
            ActiveSemesters,
            (ActiveSemesters.year == Semesters.year)
            & (ActiveSemesters.season == Semesters.season),
        )
        .join(Opportunities, Opportunities.opp_id == ActiveSemesters.opportunity_id)
        .filter(Opportunities.opp_id == opp_id)
        .order_by(Semesters.year)
    )
    pass


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/opportunities")
def positions():
    # pass objects into render_template. For example:
    # lines = ...
    # return render_template("opportunitys.html", lines=lines)

    """
    For each opportunity summary:
        name of opportunity,
        description,
        recommended majors,
        lab runners promoting,
        all forms of compensation,
    Return only opportunities active in any given semester
    """

    # Requires application logic to update current semester
    current_semester = (2023, "Fall")

    TURN_OFF_SEMESTER_FILTER = False
    active_opp_ids = (
        db.session.query(Opportunities.opp_id)
        .join(ActiveSemesters, ActiveSemesters.opportunity_id == Opportunities.opp_id)
        .filter(
            (ActiveSemesters.year == current_semester[0])
            & (ActiveSemesters.season == current_semester[1])
            | TURN_OFF_SEMESTER_FILTER
        )
        .order_by(Opportunities.opp_id)
    )

    names = (
        db.session.query(Opportunities.name)
        .join(ActiveSemesters, ActiveSemesters.opportunity_id == Opportunities.opp_id)
        .filter(
            (ActiveSemesters.year == current_semester[0])
            & (ActiveSemesters.season == current_semester[1])
            | TURN_OFF_SEMESTER_FILTER
        )
        .order_by(Opportunities.opp_id)
    )

    descriptions = (
        db.session.query(Opportunities.description)
        .join(ActiveSemesters, ActiveSemesters.opportunity_id == Opportunities.opp_id)
        .filter(
            (ActiveSemesters.year == current_semester[0])
            & (ActiveSemesters.season == current_semester[1])
            | TURN_OFF_SEMESTER_FILTER
        )
        .order_by(Opportunities.opp_id)
    )

    majors = list()
    promoters = list()
    credits = list()
    salaries = list()
    upfront_pay = list()

    for opp_id in active_opp_ids.all():
        # Access via opp_id[0]
        majors.append(get_opportunity_recommended_majors(opp_id[0]))
        promoters.append(get_opportunity_promoters(opp_id[0]))
        credits.append(get_opportunity_course_credits(opp_id[0]))
        salaries.append(get_opportunity_hourly_rates(opp_id[0]))
        upfront_pay.append(get_opportunity_upfront_pay(opp_id[0]))

    print(active_opp_ids.all())
    print(names.all())
    print(descriptions.all())
    for eachlist in [majors, promoters, credits, salaries, upfront_pay]:
        print("-" * 32)
        for each in eachlist:
            print(each.all())

    """
    result = joined_query1.all()
    joined_query1_rows = [", ".join(str(row).split(",")) for row in result]
    """

    return render_template(
        "opportunitys.html",
        names=names,
        descriptions=descriptions,
        majors=majors,
        promoters=promoters,
        credits=credits,
        salaries=salaries,
        upfront_pay=upfront_pay,
    )


@main_blueprint.route("/opportunity/<int:id>")
def opportunity(id: int):
    promoters_attr_names = ["rcs_id", "name"]

    promoters = get_opportunity_promoters(id).all()

    # Columns "course_code", "course_name"
    recommended_courses = get_opportunity_recommended_courses(id).all()

    # Columns "major_code", "major_name"
    recommended_majors = get_opportunity_recommended_majors(id).all()

    # Columns "class_year", "class_name"
    recommended_class_years = get_opportunity_recommended_class_years(id).all()

    # Columns "usd_per_hour"
    salaries = get_opportunity_hourly_rates(id).all()

    # Columns "usd"
    upfront_pay = get_opportunity_upfront_pay(id).all()

    # Columns "course_code", "number_of_credits"
    course_credits = get_opportunity_course_credits(id).all()

    # Columns "date"
    application_due_dates = get_opportunity_application_due_dates(id).all()

    # Columns "year", "season"
    active_semesters = get_opportunity_active_semesters(id).all()

    return render_template(
        "opportunity_details.html",
        promoters_attr_names=promoters_attr_names,
        promoters=promoters,
        recommended_courses=recommended_courses,
        recommended_majors=recommended_majors,
        recommended_class_years=recommended_class_years,
        salaries=salaries,
        upfront_pay=upfront_pay,
        course_credits=course_credits,
        application_due_dates=application_due_dates,
        active_semesters=active_semesters,
    )


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
