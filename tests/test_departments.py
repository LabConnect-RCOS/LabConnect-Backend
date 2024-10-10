"""
Test department routes
"""

from flask import json
from flask.testing import FlaskClient
import pytest


@pytest.mark.parametrize(
    "expected_departments",
    [
        (
            (
                "Computer Science",
                "Biology",
                "Materials Engineering",
                "Math",
                "Environmental Engineering",
                "Aerospace Engineering",
                "Aeronautical Engineering",
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
    ],
)
def test_departments_route(test_client: FlaskClient, expected_departments) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/departments' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/departments")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for department in json_data:
        assert department["name"] in expected_departments[0]
        assert department["description"] in expected_departments[1]


@pytest.mark.parametrize(
    "input_data, expected_data",
    [
        (
            {"department": "Computer Science"},
            {
                "name": "Computer Science",
                "description": "DS",
                "school_id": "School of Science",
                "professors": [
                    {"name": "Duy Le", "rcs_id": "led"},
                    {"name": "Rafael", "rcs_id": "cenzar"},
                    {"name": "Turner", "rcs_id": "turner"},
                    {"name": "Kuzmin", "rcs_id": "kuzmin"},
                    {"name": "Goldschmidt", "rcs_id": "goldd"},
                ],
                "opportunities": [
                    {"id": 1, "name": "Automated Cooling System"},
                    {"id": 2, "name": "Iphone 15 durability test"},
                ],
            },
        )
    ],
)
def test_department_route(test_client: FlaskClient, input_data, expected_data) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json=input_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert json_data["name"] == expected_data["name"]
    assert json_data["description"] == expected_data["description"]
    assert json_data["school_id"] == expected_data["school_id"]

    for prof in json_data["professors"]:
        assert prof["name"] in [p["name"] for p in expected_data["professors"]]
        assert prof["rcs_id"] in [p["rcs_id"] for p in expected_data["professors"]]

    for opportunity in json_data["opportunities"]:
        assert opportunity["id"] in [o["id"] for o in expected_data["opportunities"]]
        assert opportunity["name"] in [o["name"] for o in expected_data["opportunities"]]


@pytest.mark.parametrize(
    "input_data",
    [
        (None,),  # Testing with no JSON
        ({"wrong": "wrong"},)  # Testing with incorrect JSON
    ],
)
def test_department_route_invalid_json(test_client: FlaskClient, input_data) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json=input_data)

    assert response.status_code == 400
