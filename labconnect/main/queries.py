from labconnect import db
from labconnect.models import (
    ClassYears,
    Courses,
    Majors,
    Opportunities,
    Promotes,
    RecommendsClassYears,
    RecommendsCourses,
    RecommendsMajors,
)

# def get_opportunities_rows():
#     """
#     @RETURNS: a Query to all rows of the opportunites table, for all attributes.
#     """
#     return db.session.query(
#         Opportunities.opp_id,
#         Opportunities.name,
#         Opportunities.description,
#         Opportunities.active_status,
#         Opportunities.recommended_experience,
#     )


def get_opportunity_promoters(opp_id):
    return None
    # """
    # @PARAMETERS: opp_id: an opportunity id from the database
    # @REQUIRES: opp_id is an integer
    # @RETURNS: a Query to rows of the lab_runner table for all attributes, representing:
    #     everything about lab runners that promote the opportunity
    # """
    # return (
    #     db.session.query(LabRunner.rcs_id, LabRunner.name)
    #     .join(Promotes, Promotes.lab_runner_rcs_id == LabRunner.rcs_id)
    #     .join(Opportunities, Opportunities.opp_id == Promotes.opportunity_id)
    #     .filter(Opportunities.opp_id == opp_id)
    #     .order_by(LabRunner.name)
    # )


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


def get_opportunity_recommended_class_years(opp_id):
    """
    @PARAMETERS: opp_id: an opportunity id from the database
    @REQUIRES: opp_id is an integer
    @RETURNS: a Query to rows of the class_years table for all attributes, representing:
        everything about class years recommended by the opportunity
    """
    return (
        db.session.query(ClassYears.class_year)
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


def get_opportunity_hourly_rates(opp_id):
    return None
    # """
    # @PARAMETERS: opp_id: an opportunity id from the database
    # @REQUIRES: opp_id is an integer
    # @RETURNS: a Query to rows of the salary_comp_info table for all attributes, representing:
    #     everything about hourly salary of the opportunity
    # """
    # return (
    #     db.session.query(SalaryCompInfo.usd_per_hour)
    #     .join(HasSalaryComp, HasSalaryComp.usd_per_hour == SalaryCompInfo.usd_per_hour)
    #     .join(Opportunities, Opportunities.opp_id == HasSalaryComp.opportunity_id)
    #     .filter(Opportunities.opp_id == opp_id)
    #     .order_by(SalaryCompInfo.usd_per_hour)
    # )


def get_opportunity_upfront_pay(opp_id):
    return None
    # """
    # @PARAMETERS: opp_id: an opportunity id from the database
    # @REQUIRES: opp_id is an integer
    # @RETURNS: a Query to rows of the upfront_pay_comp_info table for all attributes, representing:
    #     everything about upfront pay of the opportunity
    # """
    # return (
    #     db.session.query(UpfrontPayCompInfo.usd)
    #     .join(HasUpfrontPayComp, HasUpfrontPayComp.usd == UpfrontPayCompInfo.usd)
    #     .join(Opportunities, Opportunities.opp_id == HasUpfrontPayComp.opportunity_id)
    #     .filter(Opportunities.opp_id == opp_id)
    #     .order_by(UpfrontPayCompInfo.usd)
    # )


def get_opportunity_course_credits(opp_id):
    return None
    # """
    # @PARAMETERS: opp_id: an opportunity id from the database
    # @REQUIRES: opp_id is an integer
    # @RETURNS: a Query to rows of the credit_comp_info table for all attributes, representing:
    #     everything about which courses are credited, and range of credits awarded by the opportunity
    # """
    # return (
    #     db.session.query(CreditCompInfo.course_code, CreditCompInfo.number_of_credits)
    #     .join(
    #         HasCreditComp,
    #         (HasCreditComp.course_code == CreditCompInfo.course_code)
    #         & (HasCreditComp.number_of_credits == CreditCompInfo.number_of_credits),
    #     )
    #     .join(Opportunities, Opportunities.opp_id == HasCreditComp.opportunity_id)
    #     .filter(Opportunities.opp_id == opp_id)
    #     .order_by(CreditCompInfo.number_of_credits)
    # )


def get_opportunity_application_due_dates(opp_id):
    return None
    # """
    # @PARAMETERS: opp_id: an opportunity id from the database
    # @REQUIRES: opp_id is an integer
    # @RETURNS: a Query to rows of the application_due_dates table for all attributes, representing:
    #     everything about the opportunity's application due dates
    # """
    # return (
    #     db.session.query(ApplicationDueDates.date)
    #     .join(ApplicationDue, ApplicationDue.date == ApplicationDueDates.date)
    #     .join(Opportunities, Opportunities.opp_id == ApplicationDue.opportunity_id)
    #     .filter(Opportunities.opp_id == opp_id)
    #     .order_by(ApplicationDueDates.date)
    # )


def get_opportunity_active_semesters(opp_id):
    return None
    # """
    # @PARAMETERS: opp_id: an opportunity id from the database
    # @REQUIRES: opp_id is an integer
    # @RETURNS: a Query to rows of the semesters table for all attributes, representing:
    #     everything about the opportunity's active semesters
    # """
    # return (
    #     db.session.query(Semesters.year, Semesters.season)
    #     .join(
    #         ActiveSemesters,
    #         (ActiveSemesters.year == Semesters.year)
    #         & (ActiveSemesters.season == Semesters.season),
    #     )
    #     .join(Opportunities, Opportunities.opp_id == ActiveSemesters.opportunity_id)
    #     .filter(Opportunities.opp_id == opp_id)
    #     .order_by(Semesters.year)
    # )
