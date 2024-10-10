"""
Test user routes
"""

from flask import json
from flask.testing import FlaskClient
import pytest


@pytest.mark.parametrize(
    "user_id, expected_status_code, expected_data",
    [
        (
            1,
            200,
            {
                "id": 1,
                "first_name": "Rafael",
                "last_name": "Cenzano",
                "preferred_name": "Raf",
                "email": "cenzar@rpi.edu",
                "departments": [
                    {"user_id": 1, "department_id": "Computer Science"},
                    {"user_id": 1, "department_id": "Math"},
                ],
                "majors": [
                    {"user_id": 1, "major_code": "CSCI"},
                    {"user_id": 1, "major_code": "MATH"},
                ],
                "courses": [
                    {"in_progress": False, "user_id": 1, "course_code": "CSCI2300"},
                    {"in_progress": True, "user_id": 1, "course_code": "CSCI4430"},
                ],
            },
        ),
        (
            2,
            200,
            {
                "id": 2,
                "first_name": "RCOS",
                "last_name": "RCOS",
                "preferred_name": None,
                "email": "test@rpi.edu",
                "departments": [
                    {"department_id": "Computer Science", "user_id": 2},
                ],
                "majors": [
                    {"user_id": 2, "major_code": "CSCI"},
                ],
                "courses": [
                    {"in_progress": False, "user_id": 2, "course_code": "CSCI2300"},
                ],
            },
        ),
    ]
)
def test_user_route_with_input(test_client: FlaskClient, user_id, expected_status_code, expected_data) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response and data are valid
    """
    response = test_client.get("/user", json={"id": str(user_id)})
    assert response.status_code == expected_status_code

    json_data = json.loads(response.data)
    assert json_data == expected_data


@pytest.mark.parametrize(
    "user_id, expected_status_code, expected_opportunities",
    [
        (
            1,
            200,
            [
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
            ],
        ),
        (
            2,
            200,
            [
                (
                    "Checking out cubes",
                    "Material Sciences",
                    "Experienced in materials.",
                    None,
                    "Fall",
                    2024,
                    True,
                ),
                (
                    "Test the water",
                    "Testing the quality of water in Troy pipes",
                    "Understanding of lead poisoning",
                    None,
                    "Summer",
                    2024,
                    True,
                ),
            ],
        ),
    ],
)
def test_user_opportunity_cards(test_client: FlaskClient, user_id, expected_status_code, expected_opportunities) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the opportunity cards are valid
    """
    response = test_client.get("/user", json={"id": user_id})
    assert response.status_code == expected_status_code

    json_data = json.loads(response.data)
    for i, item in enumerate(json_data["opportunities"]):
        assert item["name"] == expected_opportunities[i][0]
        assert item["description"] == expected_opportunities[i][1]
        assert item["recommended_experience"] == expected_opportunities[i][2]
        assert item["pay"] == expected_opportunities[i][3]
        assert item["semester"] == expected_opportunities[i][4]
        assert item["year"] == expected_opportunities[i][5]
        assert item["active"] == expected_opportunities[i][6]


def test_user_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET) with no JSON payload
    THEN check that the response is a 400 error
    """
    response = test_client.get("/user")
    assert response.status_code == 400


def test_user_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET) with incorrect JSON payload
    THEN check that the response is a 400 error
    """
    response = test_client.get("/user", json={"wrong": "wrong"})
    assert response.status_code == 400


def test_user_not_found(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET) with a non-existent user ID
    THEN check that the response is a 404 error
    """
    response = test_client.get("/user", json={"id": "not found"})
    assert response.status_code == 404
