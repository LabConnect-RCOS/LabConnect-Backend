import json

"""
Test mains
"""

from flask import json
from flask.testing import FlaskClient
import json


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
    response = test_client.get("/profile")
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
    assert b"Name:" in response.data
    assert b"Department:" in response.data
    assert b"Contact:" in response.data
=======
>>>>>>> f022e2c (Updated queries)
    assert data["Profile"]["rcs_id"] == "turnerw"
    assert data["Profile"]["name"] == "Turner"
    assert data["Profile"]["email"] == "turnerw@rpi.edu"
    assert data["Profile"]["phone_number"] == "123-456-7890"
    assert data["Profile"]["website"] == "turnerw.com"
    assert data["Profile"]["title"] == "Professor"
    assert data["Profile"]["departments"] == "CSCI"
    assert data["Profile"]["past_opportunities"][0]["professor"] == "Kuzman"
    assert data["Profile"]["past_opportunities"][0]["credits"] == 4
    assert data["Profile"]["past_opportunities"][0]["description"] == "RCOS"
    assert data["Profile"]["current_opportunities"][0]["professor"] == "Xiao"
    assert data["Profile"]["current_opportunities"][0]["credits"] == 4
    assert (
        data["Profile"]["current_opportunities"][0]["description"] == "DataStructures"
    )
<<<<<<< HEAD
=======


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
>>>>>>> 01b2433 (Updated queries)
>>>>>>> f022e2c (Updated queries)
=======
    assert b"Name:" in response.data
    assert b"Department:" in response.data
    assert b"Contact:" in response.data
>>>>>>> e389a38 (Rebase)
