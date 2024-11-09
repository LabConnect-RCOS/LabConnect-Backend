"""
Test lab manager routes
"""

from flask import json
from flask.testing import FlaskClient


def test_lab_manager_route_with_input_id(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager", json={"rcs_id": "cenzar"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    cenzar_data = {
        "website": None,
        "rcs_id": "cenzar",
        "name": "Rafael",
        "alt_email": None,
        "phone_number": None,
        "email": None,
        "description": None,
    }

    assert json_data == cenzar_data


def test_lab_manager_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager")

    assert response.status_code == 400


def test_lab_manager_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager", json={"wrong": "wrong"})

    assert response.status_code == 400


def test_lab_manager_opportunity_cards(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager/opportunities", json={"rcs_id": "cenzar"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    lab_manager_opportunities_data = (
        (
            "Automated Cooling System",
            "Energy efficient AC system",
            "Thermodynamics",
            15.0,
            "Spring",
            2024,
            True,
        ),
        (
            "Iphone 15 durability test",
            "Scratching the Iphone, drop testing etc.",
            "Experienced in getting angry and throwing temper tantrum",
            None,
            "Spring",
            2024,
            True,
        ),
    )

    for i, item in enumerate(json_data["cenzar"]):
        assert item["name"] == lab_manager_opportunities_data[i][0]
        assert item["description"] == lab_manager_opportunities_data[i][1]
        assert item["recommended_experience"] == lab_manager_opportunities_data[i][2]
        assert item["pay"] == lab_manager_opportunities_data[i][3]
        assert item["semester"] == lab_manager_opportunities_data[i][4]
        assert item["year"] == lab_manager_opportunities_data[i][5]
        assert item["active"] == lab_manager_opportunities_data[i][6]


def test_lab_manager_opportunity_cards_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager/opportunities")

    assert response.status_code == 400


def test_lab_manager_opportunity_cards_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager/opportunities", json={"wrong": "wrong"})

    assert response.status_code == 400
