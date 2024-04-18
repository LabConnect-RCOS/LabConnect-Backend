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


def test_professor_profile(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorProfile/cenzar")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data)

    # Test that the "name" key exists
    assert "name" in data
    assert "image" in data
    assert "department" in data
    assert "description" in data
    assert "role" in data
    assert "phone_number" in data
    assert "email" in data
    assert "alt_email" in data
    assert "website" in data
    assert "phone" in data
    assert "role" in data


def test_professor_opportunity_cards(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorOpportunityCards/led")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))

    # Test that the "name" key exists
    assert len(data.keys()) > 0
    for eachCard in data["data"]:
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

    response = test_client.get("/getOpportunityMeta/1", content_type="application/json")

    # assert response.status_code == 200

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
        # assert "credits" in opportunity
        assert "semester" in opportunity
        assert "year" in opportunity
        assert "application_due" in opportunity
        assert "active" in opportunity
        #assert "professor" in opportunity
        #assert "department" in opportunity


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
        "name": "Some test opportunity",
        "description": "Some test description",
        "recommended_experience": "Some test experience",
        "pay": 25.0,
        "credits": ["1", "2", "3", "4"],
        "semester": "FALL",
        "year": 2024,
        "application_due": "2024-03-30",
        "active": True,
        "courses": ["CSCI4430"],
        "majors": ["BIOL"],
        "years": [2023, 2024],
        "active": True,
    }

    response = test_client.post(
        "/createOpportunity",
        data=json.dumps(test_data),
        content_type="application/json",
    )

    assert response.status_code == 200


# def test_schools_and_departments(test_client: FlaskClient) -> None:
#     response = test_client.get(
#         "/getSchoolsAndDepartments", content_type="application/json"
#     )

#     assert response.status_code == 200

#     data = json.loads(response.data.decode("utf-8"))

#     assert "School of Science" in data
#     assert "School of Engineering" in data

#     query = db.session.execute(
#         db.select(RPISchools, RPIDepartments).join(
#             RPIDepartments, RPISchools.name == RPIDepartments.school_id
#         )
#     )

#     results = query.all()

#     # check that all the schools and department are in the data and are accurate
#     for tuple in results:
#         assert tuple[1].name in data[tuple[0].name]
