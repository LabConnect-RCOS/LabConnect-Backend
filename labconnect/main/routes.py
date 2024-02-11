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
from labconnect.models import Opportunities

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


@main_blueprint.route("/department/<string:department>")
def department(department: str):
    return render_template("department.html")


@main_blueprint.route("/discover")
def discover():
    return render_template("discover.html")


@main_blueprint.route("/getOpportunity/<string:opp_id>", methods=["GET"])
def getOpportunity(opp_id:str):
    if request.method == "GET":
        # query database for opportunity
        
        # return data in the below format if opportunity is found
        return {
            "id": "u1",
            "title": 'Software Engineer',
            "department": "Computer Science",
            "location": "Sage Hall",
            "date": "2024-02-23",
            "author": "John Doe",
            "credits": 2,
            "description" : "This is a description",
            "id" : "",
            "salary": 15,
            "upfrontPay": 200,
            "years" : ['Freshman', 'Junior', 'Sophomore']
        }
    
    abort(500)

# getting information about professors in staff profile pages
    
@main_blueprint.route("/getProfessorProfile/<string:rcs_id>", methods=["GET"])
def getProfessorProfile(rcs_id: str):
    # test code until database code is added
    if request.method == "GET":
        return {
            rcs_id: {
                "name": "Peter Johnson",
                "image": "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
                "researchCenter": "Computational Fake Center",
                "department": "Computer Science",
                "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
        pharetra sit amet aliquam id diam maecenas ultricies mi. Montes
        nascetur ridiculus mus mauris vitae ultricies leo. Porttitor massa
        id neque aliquam. Malesuada bibendum arcu vitae elementum. Nulla
        aliquet porrsus mattis molestie aiaculis at erat pellentesque. 
        At risus viverra adipiscing at.
        Tincidunt tortor aliquam nulla facilisi cras fermentum odio eu
        feugiat. Eget fUt eu sem integer vitae justo
        eget magna fermentum. Lobortis feugiat vivamus at augue eget arcu
        dictum. Et tortor at risus viverra adipiscing at in tellus.
        Suspendisse sed nisi lacus sed viverra tellus. Potenti nullam ac
        tortor vitae. Massa id neque aliquam vestibulum. Ornare arcu odio ut
        sem nulla pharetra. Quam id leo in vitae turpis massa. Interdum
        velit euismod in pellentesque massa placerat duis ultricies lacus.
        Maecenas sed enim ut sem viverra aliquet eget sit amet. Amet
        venenatis urna cursus eget nunc scelerisque viverra mauris. Interdum
        varius sit amet mattis. Aliquet nec ullamcorper sit amet risus
        nullam. Aliquam faucibus purus in massa tempor nec feugiat. Vitae
        turpis massa sed elementum tempus. Feugiat in ante metus dictum at
        tempor. Malesuada nunc vel risus commodo viverra maecenas accumsan.
        Integer vitae justo.""",
            },
        }

    abort(500)

@main_blueprint.route("/getProfessorOpportunityCards/<string:rcs_id>", methods=["GET"])
def getProfessorOpportunityCards(rcs_id: str):
    # test code until database code is added
    if request.method == "GET":

        # query database for opportunities

        # return opportunities
        return {
            rcs_id: [
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o1",
                },
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o2",
                },
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o3",
                },
                {
                    "title": "Chemistry Intern",
                    "body": "Due February 15, 2023",
                    "attributes": ["Remote", "Paid", "Credits"],
                    "id": "o4",
                },
            ]
        }
    abort(500)

@main_blueprint.route("/getProfessorMeta", methods=["GET"])
def getProfessorMeta():
    if request.method == "GET":
        data = request.json

        user_id = data["user_id"]
        auth_token = data["authToken"]

        # query database to match user id and password from data received
        
        # if match, return user data
        # more fields to be added here later
        
        return {
            "name": "Dr. Peter Johnson",
            "department": "Computer Science",
            "researchCenter": "Computational Fake Center",
            "email": "johnj@rpi.edu",
            "phone": "518-123-4567",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do""",
            "image": "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
        }

    abort(500)

#_______________________________________________________________________________________________#

# Editing Opportunities in Profile Page
    
@main_blueprint.route("/deleteOpportunity", methods=["DELETE", "POST"])
def deleteOpportunity():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        postID = data["postID"]
        authToken = data["authToken"]
        authorID = data["authToken"]
        
        # query database to see if the credentials above match
        
        
        # if match is found, delete the opportunity, return status 200
        
        abort(200)
        
    abort(500)

@main_blueprint.route("/changeActiveStatus", methods=["DELETE", "POST"])
def changeActiveStatus():
    if request.method in ["DELETE", "POST"]:
        data = request.json
        postID = data["postID"]
        authToken = data["authToken"]
        authorID = data["authToken"]
        setStatus = data["setStatus"]
        
        # query database to see if the credentials above match
        
        
        # if match is found, change the opportunities active status to true or false based on setStatus
        
        abort(200)
        
    abort(500)


@main_blueprint.route("/create_post", methods=["POST"])
def create_post():
    if request.method=="POST":
        return "Creating POST"
    
    abort(500)


@main_blueprint.route("/login")
def login():
    return render_template("sign_in.html")