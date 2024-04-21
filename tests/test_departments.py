"""
Test department routes
"""

from flask import json
from flask.testing import FlaskClient


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
        (
            "Computer Science",
            "Biology",
            "Materials Engineering",
            "Math",
            "Environmental Engineering",
            "Aerospace Engineering",
            "Areonautical Engineering",
        ),
        (
            "DS",
            "life",
            "also pretty cool",
            "quick maths",
            "water",
            "space, the final frontier",
            "flying, need for speed",
        ),
    )

    for department in json_data:
        assert department["name"] in rpi_departments_data[0]
        assert department["description"] in rpi_departments_data[1]


def test_department_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json={"department": "Computer Science"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert json_data["name"] == "Computer Science"
    assert json_data["description"] == "DS"
    assert json_data["school_id"] == "School of Science"

    prof_names = ["Duy Le", "Rafael", "Turner", "Kuzmin", "Goldschmidt"]
    prof_rcs_ids = ["led", "cenzar", "turner", "kuzmin", "goldd"]

    for prof in json_data["professors"]:
        assert prof["name"] in prof_names
        assert prof["rcs_id"] in prof_rcs_ids

    opportunity_ids = [1, 2]
    opportunity_names = ["Automated Cooling System", "Iphone 15 durability test"]

    for opportunity in json_data["opportunities"]:
        assert opportunity["id"] in opportunity_ids
        assert opportunity["name"] in opportunity_names


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
