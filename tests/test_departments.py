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
        ("Computer Science", "Biology", "Materials Engineering"),
        ("DS", "life", "also pretty cool"),
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
