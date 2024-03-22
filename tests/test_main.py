import json

"""
Test mains
"""

from flask import json
from flask.testing import FlaskClient
from labconnect.helpers import SemesterEnum
from datetime import date

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

    response = test_client.get("/getProfessorProfile/d1")
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
    response = test_client.get("/getOpportunity/o1")

    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))

    # Test that the "name" key exists
    assert "title" in data
    assert "location" in data
    assert "date" in data
    assert "author" in data
    assert "credits" in data  # and data["credits"] is int
    assert "description" in data  # and data["description"] is str
    assert "salary" in data  # and data["salary"] is int
    assert "upfrontPay" in data  # and data["upfrontPay"] is int
    assert "years" in data  # and data["years"] is list


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
    WHEN the '/department/<department>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_profile_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/profile", json={"input": "rcs_id"})
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200

    json_data = json.loads(response.data)

    profile_data = (
        ("led", "cenzar"),
        ("Duy Lee", "Rafael"),
        ("Computer Science", "Computer Science"),
    )

    opportunity_data = (            
        (
            "Automated Cooling System",
            "Energy efficient AC system",
            "Thermodynamics",
            15.0,
            "4",
            SemesterEnum.SPRING,
            2024,
            date.today(),
            True,
        ),
        (
            "Iphone 15 durability test",
            "Scratching the Iphone, drop testing etc.",
            "Experienced in getting angry and throwing temper tantrum",
            None,
            "1,2,3,4",
            SemesterEnum.SPRING,
            2024,
            date.today(),
            True,
        ),
    )

    print(json_data)
    for i, lab_manager in enumerate(json_data):
        assert lab_manager["rcs_id"] == profile_data[0][i]
        assert lab_manager["name"] == profile_data[1][i]
        assert lab_manager["department_id"] == profile_data[2][i]

    for i, opportunity in enumerate(json_data):
        assert opportunity["name"] == opportunity_data[i][0]
        assert opportunity["description"] == opportunity_data[i][1]
        assert opportunity["recommended_experience"] == opportunity_data[i][2]
        assert opportunity["pay"] == opportunity_data[i][3]
        assert opportunity["credits"] == opportunity_data[i][4]
        assert opportunity["semester"] == opportunity_data[i][5]
        assert opportunity["year"] == opportunity_data[i][6]
        assert opportunity["application_due"] == opportunity_data[i][7]
        assert opportunity["active"] == opportunity_data[i][8]


def test_tips_and_tricks_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/tips")
    assert response.status_code == 200
    assert b"Tips and Tricks for LabConnect" in response.data


def test_info_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/info")
    assert response.status_code == 200
    assert b"URP for Credit" in response.data
    assert b"URP for Funding" in response.data

    response = test_client.get("/information")
    assert response.status_code == 200
    assert b"URP for Credit" in response.data
    assert b"URP for Funding" in response.data
    assert b"Name:" in response.data
    assert b"Department:" in response.data
    assert b"Contact:" in response.data
