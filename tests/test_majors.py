"""
Test majors routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "expected_majors",
    [
        (
            ("CSCI", "ECSE", "BIOL", "MATH", "COGS"),
            (
                "Computer Science",
                "Electrical, Computer, and Systems Engineering",
                "Biological Science",
                "Mathematics",
                "Cognitive Science",
            ),
        )
    ],
)
def test_majors_route(test_client: FlaskClient, expected_majors) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for major in json_data:
        assert major["code"] in expected_majors[0]
        assert major["name"] in expected_majors[1]


@pytest.mark.parametrize(
    "input_data, expected_majors",
    [
        (
            {"input": "computer"},
            (
                ("CSCI", "ECSE"),
                (
                    "Computer Science",
                    "Electrical, Computer, and Systems Engineering",
                ),
            ),
        ),
    ],
)
def test_majors_route_with_input_name(
    test_client: FlaskClient, input_data, expected_majors
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json=input_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for i, major in enumerate(json_data):
        assert major["code"] == expected_majors[0][i]
        assert major["name"] == expected_majors[1][i]


@pytest.mark.parametrize(
    "input_data, expected_majors",
    [
        (
            {"input": "cs"},
            (
                ("CSCI", "ECSE", "MATH"),
                (
                    "Computer Science",
                    "Electrical, Computer, and Systems Engineering",
                    "Mathematics",
                ),
            ),
        ),
    ],
)
def test_majors_route_with_input_code(
    test_client: FlaskClient, input_data, expected_majors
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json=input_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for i, major in enumerate(json_data):
        assert major["code"] == expected_majors[0][i]
        assert major["name"] == expected_majors[1][i]
