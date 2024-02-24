from flask import abort, render_template, request

from labconnect import db
from labconnect.helpers import SemesterEnum
from labconnect.models import Opportunities

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


@main_blueprint.route("/getOpportunity/<string:opp_id>", methods=["GET"])
def getOpportunity(opp_id: str):
    if request.method == "GET":
        # query database for opportunity

        # return data in the below format if opportunity is found
        return {
            "id": "u1",
            "title": "Software Engineer",
            "department": "Computer Science",
            "location": "Sage Hall",
            "date": "2024-02-23",
            "author": "John Doe",
            "credits": 2,
            "description": "This is a description",
            "salary": 15,
            "upfrontPay": 200,
            "years": ["Freshman", "Junior", "Sophomore"],
        }

    abort(500)


@main_blueprint.route("/getProfessorProfile/<string:rcs_id>", methods=["GET"])
def getProfessorProfile(rcs_id: str):
    # test code until database code is added
    if request.method == "GET":
        return {
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


# _______________________________________________________________________________________________#

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
    return "Creating POST"


@main_blueprint.route("/login")
def login():
    return render_template("sign_in.html")


@main_blueprint.route("/500")
def force_error() -> str:
    return str(10 / 0)
