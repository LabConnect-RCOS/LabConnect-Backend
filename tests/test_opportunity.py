"""
Test opportunity routes
"""

import json

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


def test_get_opportunity(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET)
    THEN check that the response is valid
    """
    response1 = test_client.get("/opportunity", json={"id": 1})
    response2 = test_client.get("/opportunity", json={"id": 2})

    assert response1.status_code == 200
    assert response2.status_code == 200

    json_data1 = json.loads(response1.data)
    json_data2 = json.loads(response2.data)

    lab_manager_opportunities_data = (
        (
            "Automated Cooling System",
            "Energy efficient AC system",
            "Thermodynamics",
            15.0,
            False,
            False,
            False,
            True,
            "Spring",
            2024,
            True,
        ),
        (
            "Iphone 15 durability test",
            "Scratching the Iphone, drop testing etc.",
            "Experienced in getting angry and throwing temper tantrum",
            None,
            True,
            True,
            True,
            True,
            "Spring",
            2024,
            True,
        ),
    )

    assert json_data1["name"] == lab_manager_opportunities_data[0][0]
    assert json_data1["description"] == lab_manager_opportunities_data[0][1]
    assert json_data1["recommended_experience"] == lab_manager_opportunities_data[0][2]
    assert json_data1["pay"] == lab_manager_opportunities_data[0][3]
    assert json_data1["one_credit"] == lab_manager_opportunities_data[0][4]
    assert json_data1["two_credits"] == lab_manager_opportunities_data[0][5]
    assert json_data1["three_credits"] == lab_manager_opportunities_data[0][6]
    assert json_data1["four_credits"] == lab_manager_opportunities_data[0][7]
    assert json_data1["semester"] == lab_manager_opportunities_data[0][8]
    assert json_data1["year"] == lab_manager_opportunities_data[0][9]
    assert json_data1["active"] == lab_manager_opportunities_data[0][10]

    assert json_data2["name"] == lab_manager_opportunities_data[1][0]
    assert json_data2["description"] == lab_manager_opportunities_data[1][1]
    assert json_data2["recommended_experience"] == lab_manager_opportunities_data[1][2]
    assert json_data2["pay"] == lab_manager_opportunities_data[1][3]
    assert json_data2["one_credit"] == lab_manager_opportunities_data[1][4]
    assert json_data2["two_credits"] == lab_manager_opportunities_data[1][5]
    assert json_data2["three_credits"] == lab_manager_opportunities_data[1][6]
    assert json_data2["four_credits"] == lab_manager_opportunities_data[1][7]
    assert json_data2["semester"] == lab_manager_opportunities_data[1][8]
    assert json_data2["year"] == lab_manager_opportunities_data[1][9]
    assert json_data2["active"] == lab_manager_opportunities_data[1][10]

    print(json_data2)


def test_get_opportunity_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/opportunity")

    assert response.status_code == 400


def test_opportunity_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/opportunity", json={"wrong": "wrong"})

    assert response.status_code == 400


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
        # assert "professor" in opportunity
        # assert "department" in opportunity


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
        "location": "TBD",
    }

    response = test_client.post(
        "/createOpportunity",
        data=json.dumps(test_data),
        content_type="application/json",
    )

    assert response.status_code == 200

    # query database to check for new opportunity with the same name
    query = db.session.query(Opportunities).filter(
        Opportunities.name == "Some test opportunity",
        Opportunities.description == "Some test description",
        Opportunities.recommended_experience == "Some test experience",
    )

    data = query.first()
    assert data is not None
    id = data.id

    # delete the opportunity by sending request to deleteOpportunity
    response = test_client.post(
        "/deleteOpportunity",
        data=json.dumps({"id": id}),
        content_type="application/json",
    )

    assert response.status_code == 200

    # check that the opportunity was deleted
    query = db.session.query(Opportunities).filter(Opportunities.id == id)
    assert query.first() is None


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
