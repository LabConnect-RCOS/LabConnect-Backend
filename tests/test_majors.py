"""
Test majors routes
"""

from flask import json
from flask.testing import FlaskClient


def test_majors_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE", "BIOL", "MATH", "COGS"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
            "Biological Science",
            "Mathematics",
            "Cognitive Science",
        ),
    )

    for major in json_data:
        assert major["code"] in majors_data[0]
        assert major["name"] in majors_data[1]


def test_majors_route_with_input_name(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json={"input": "computer"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
        ),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == majors_data[0][i]
        assert major["name"] == majors_data[1][i]


def test_majors_route_with_input_code(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json={"input": "cs"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE", "MATH"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
            "Mathematics",
        ),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == majors_data[0][i]
        assert major["name"] == majors_data[1][i]
