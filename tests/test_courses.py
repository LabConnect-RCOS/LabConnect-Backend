"""
Test courses routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "request_json, expected_status, expected_response",
    [
        (
            {"input": "data"},
            200,
            [{"code": "CSCI4390", "name": "Data Mining"}],
        ),
        (
            {"input": "cs"},
            200,
            [
                {"code": "CSCI2300", "name": "Introduction to Algorithms"},
                {"code": "CSCI2961", "name": "Rensselaer Center for Open Source"},
                {"code": "CSCI4390", "name": "Data Mining"},
                {"code": "CSCI4430", "name": "Programming Languages"},
            ],
        ),
        (None, 400, None),
        ({"wrong": "wrong"}, 400, None),
        ({"input": "not found"}, 404, None),
    ],
)
def test_courses_route(
    test_client: FlaskClient, request_json, expected_status, expected_response
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET) with various inputs
    THEN check that the response status and data are as expected
    """
    response = (
        test_client.get("/courses", json=request_json)
        if request_json
        else test_client.get("/courses")
    )

    assert response.status_code == expected_status

    if expected_response is not None:
        json_data = json.loads(response.data)
        if expected_status == 200:
            assert json_data == expected_response
        else:
            assert json_data is not None


@pytest.mark.parametrize(
    "input_name, course_data",
    [
        (
            "cs",
            (
                ("CSCI2300", "CSCI2961", "CSCI4390", "CSCI4430"),
                (
                    "Introduction to Algorithms",
                    "Rensselaer Center for Open Source",
                    "Data Mining",
                    "Programming Languages",
                ),
            ),
        )
    ],
)
def test_courses_route_with_specific_input(
    test_client: FlaskClient, input_name, course_data
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET) with specific course input names
    THEN check that the response data matches the expected courses
    """
    response = test_client.get("/courses", json={"input": input_name})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for i, course in enumerate(json_data):
        assert course["code"] == course_data[0][i]
        assert course["name"] == course_data[1][i]
