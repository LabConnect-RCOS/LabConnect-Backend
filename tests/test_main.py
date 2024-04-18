import json

"""
Test mains
"""

from flask import json
from flask.testing import FlaskClient

from labconnect import db
from labconnect.helpers import OrJSONProvider, SemesterEnum
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
)


def test_home_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_professor_profile(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorProfile/cenzar")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data)

    # Test that the "name" key exists
    assert "name" in data
    assert "image" in data
    assert "researchCenter" in data
    assert "department" in data
    assert "description" in data


def test_get_professor_meta(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/getProfessorMeta' endpoint is requested (GET) with valid data
    THEN check that the response is valid and contains expected professor data
    """

    test_data = {
        "user_id": "some_user_id",  # Replace with a valid user ID
        "authToken": "some_auth_token",  # Replace with a valid token
    }

    response = test_client.get(
        "/getProfessorMeta", data=json.dumps(test_data), content_type="application/json"
    )

    assert response.status_code == 200

    data = json.loads(response.data)

    # Assertions on the expected data
    assert "name" in data
    assert "image" in data
    assert "researchCenter" in data
    assert "department" in data
    assert "description" in data
    assert "phone" in data


def test_professor_opportunity_cards(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorOpportunityCards/d1")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))

    # Test that the "name" key exists
    assert len(data.keys()) > 0
    assert "d1" in data.keys()
    print(data)
    for eachCard in data["d1"]:
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "id" in eachCard


def test_get_opportunity(test_client: FlaskClient) -> None:
    response = test_client.get("/getOpportunity/2")

    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))
    data = data["data"]

    # Test that the "name" key exists
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "recommended_experience" in data
    assert "author" in data
    assert "department" in data
    assert "aboutSection" in data

    for eachSection in data["aboutSection"]:
        assert "title" in eachSection
        assert "description" in eachSection


def test_get_opportunity_meta(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/getOpportunityMeta' endpoint is requested (GET) with valid data
    THEN check that the response is valid and contains expected opportunity data
    """

    response = test_client.get("/getOpportunityMeta/5", content_type="application/json")

    assert response.status_code == 200

    data = json.loads(response.data)
    data = data["data"]

    # Assertions on the expected data
    assert "name" in data
    assert "description" in data
    assert "recommended_experience" in data
    assert "pay" in data
    assert "credits" in data
    assert "semester" in data
    assert "year" in data
    assert "application_due" in data
    assert "active" in data
    assert "courses" in data
    assert "majors" in data
    assert "years" in data
    assert "active" in data


def test_get_opportunity_professor(test_client: FlaskClient) -> None:
    response = test_client.get("/getOpportunityByProfessor/led")

    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))
    data = data["data"]

    # Test that the "name" key exists
    for opportunity in data:
        assert "id" in opportunity
        assert "name" in opportunity
        assert "description" in opportunity
        assert "recommended_experience" in opportunity
        assert "pay" in opportunity
        assert "credits" in opportunity
        assert "semester" in opportunity
        assert "year" in opportunity
        assert "application_due" in opportunity
        assert "active" in opportunity
        assert "professor" in opportunity
        assert "department" in opportunity


def test_get_professor_opportunity_cards(test_client: FlaskClient) -> None:
    response = test_client.get(
        "/getProfessorOpportunityCards/led", content_type="application/json"
    )

    assert response.status_code == 200

    data = json.loads(response.data.decode("utf-8"))
    data = data["data"]

    for eachCard in data:
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "id" in eachCard


def test_profile_opportunities(test_client: FlaskClient) -> None:
    response = test_client.get(
        "/getProfileOpportunities/led", content_type="application/json"
    )

    assert response.status_code == 200

    data = json.loads(response.data.decode("utf-8"))
    data = data["data"]

    for eachCard in data:
        assert "id" in eachCard
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "activeStatus" in eachCard


def test_create_opportunity(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/createOpportunity' endpoint is requested (POST) with valid data
    THEN check that the response is valid and contains expected data
    """

    test_data = {
        "authorID": "led",
        "newPostData": {
            "name": "Some test opportunity",
            "description": "Some test description",
            "recommended_experience": "Some test experience",
            "pay": 25.0,
            "credits": "4",
            "semester": "FALL",
            "year": 2024,
            "application_due": "2024-03-30",
            "active": True,
            "courses": ["CSCI4430"],
            "majors": ["BIOL"],
            "years": [2023, 2024],
        },
    }

    response = test_client.post(
        "/createOpportunity",
        data=json.dumps(test_data),
        content_type="application/json",
    )

    assert response.status_code == 200


def test_schools_and_departments(test_client: FlaskClient) -> None:
    response = test_client.get(
        "/getSchoolsAndDepartments", content_type="application/json"
    )

    assert response.status_code == 200

    data = json.loads(response.data)

    assert "School of Science" in data
    assert "School of Engineering" in data

    query = db.session.execute(
        db.select(RPISchools, RPIDepartments).join(
            RPIDepartments, RPISchools.name == RPIDepartments.school_id
        )
    )

    results = query.all()

    # check that all the schools and department are in the data and are accurate
    for tuple in results:
        assert tuple[1].name in data[tuple[0].name]


def test_discover_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/discover' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/discover")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_login_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/login")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_department_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json={"department": "Computer Science"})

    assert response.status_code == 200

    assert {"name": "Computer Science", "description": "DS"} == json.loads(
        response.data
    )


def test_department_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department")

    assert response.status_code == 400


def test_department_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json={"wrong": "wrong"})

    assert response.status_code == 400


def test_profile_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/profile/bob")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_schools_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/schools' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/schools")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    rpi_schools_data = (
        ("School of Science", "School of Engineering"),
        ("the coolest of them all", "also pretty cool"),
    )

    for school in json_data:
        assert school["name"] in rpi_schools_data[0]
        assert school["description"] in rpi_schools_data[1]


def test_departments_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/departments' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/departments")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    rpi_departments_data = (
        ("Computer Science", "Biology", "Materials Engineering"),
        ("DS", "life", "also pretty cool"),
    )

    for department in json_data:
        assert department["name"] in rpi_departments_data[0]
        assert department["description"] in rpi_departments_data[1]


def test_majors_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE", "BIOL", "MATH", "COGS"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
            "Biological Science",
            "Mathematics",
            "Cognitive Science",
        ),
    )

    for major in json_data:
        assert major["code"] in majors_data[0]
        assert major["name"] in majors_data[1]


def test_majors_route_with_input_name(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json={"input": "computer"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
        ),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == majors_data[0][i]
        assert major["name"] == majors_data[1][i]


def test_majors_route_with_input_code(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json={"input": "cs"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE", "MATH"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
            "Mathematics",
        ),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == majors_data[0][i]
        assert major["name"] == majors_data[1][i]


def test_years_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/years' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/years")

    assert response.status_code == 200

    assert [2024, 2025, 2026, 2027, 2028, 2029] == json.loads(response.data)


def test_courses_route_with_input_name(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"input": "data"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    print(json_data)

    assert json_data[0]["code"] == "CSCI4390"
    assert json_data[0]["name"] == "Data Mining"


def test_courses_route_with_input_code(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"input": "cs"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    course_data = (
        ("CSCI2961", "CSCI4390", "CSCI4430"),
        ("Rensselaer Center for Open Source", "Data Mining", "Programming Languages"),
    )

    print(json_data)

    for i, major in enumerate(json_data):
        assert major["code"] == course_data[0][i]
        assert major["name"] == course_data[1][i]


def test_courses_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses")

    assert response.status_code == 400


def test_courses_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"wrong": "wrong"})

    assert response.status_code == 400
