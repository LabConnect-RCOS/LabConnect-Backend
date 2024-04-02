"""
Test courses routes
"""

from flask import json
from flask.testing import FlaskClient


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


def test_courses_not_found(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"input": "not found"})

    print(json.loads(response.data))

    assert response.status_code == 404
