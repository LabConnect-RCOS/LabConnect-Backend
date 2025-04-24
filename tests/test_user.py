"""
Test user routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "input_data, expected_status, expected_output",
    [
        (
            {"id": "1"},
            200,
            {
                "id": 1,
                "first_name": "Rafael",
                "preferred_name": "Raf",
                "last_name": "Cenzano",
                "email": "cenzar@rpi.edu",
                "description": "labconnect is the best RCOS project",
                "profile_picture": "https://rafael.sirv.com/Images/rafael.jpeg?thumbnail=350&format=webp&q=90",
                "website": "https://rafaelcenzano.com",
                "class_year": "2025",
                "lab_manager_id": 1,
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
            {"id": "2"},
            200,
            {
                "id": 2,
                "first_name": "RCOS",
                "preferred_name": None,
                "last_name": "RCOS",
                "email": "test@rpi.edu",
                "description": None,
                "profile_picture": "https://www.svgrepo.com/show/206842/professor.svg",
                "website": None,
                "class_year": None,
                "lab_manager_id": None,
                "departments": [{"user_id": 2, "department_id": "Computer Science"}],
                "majors": [{"user_id": 2, "major_code": "CSCI"}],
                "courses": [
                    {"in_progress": False, "user_id": 2, "course_code": "CSCI2300"}
                ],
            },
        ),
    ],
)
def test_user_route(
    test_client: FlaskClient, input_data, expected_status, expected_output
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET) with input data
    THEN check that the response is valid and matches expected output
    """
    response = test_client.get("/user", json=input_data)
    assert response.status_code == expected_status
    json_data = json.loads(response.data)
    assert json_data == expected_output


@pytest.mark.parametrize(
    "input_data, expected_opportunities",
    [
        (
            {"id": 1},
            [
                {
                    "name": "Automated Cooling System",
                    "description": "Energy efficient AC system",
                    "recommended_experience": "Thermodynamics",
                    "pay": 15.0,
                    "semester": "Spring",
                    "year": 2024,
                    "active": True,
                },
                {
                    "name": "Iphone 15 durability test",
                    "description": "Scratching the Iphone, drop testing etc.",
                    "recommended_experience": "Experienced in getting angry and "
                    "throwing temper tantrum",
                    "pay": None,
                    "semester": "Spring",
                    "year": 2024,
                    "active": True,
                },
            ],
        ),
        (
            {"id": 2},
            [
                {
                    "name": "Checking out cubes",
                    "description": "Material Sciences",
                    "recommended_experience": "Experienced in materials.",
                    "pay": None,
                    "semester": "Fall",
                    "year": 2024,
                    "active": True,
                },
                {
                    "name": "Test the water",
                    "description": "Testing the quality of water in Troy pipes",
                    "recommended_experience": "Understanding of lead poisioning",
                    "pay": None,
                    "semester": "Summer",
                    "year": 2024,
                    "active": True,
                },
            ],
        ),
    ],
)
def test_user_opportunity_cards(
    test_client: FlaskClient, input_data, expected_opportunities
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET) with input data
    THEN check that the opportunity cards in the response are valid
    """
    response = test_client.get("/user", json=input_data)
    assert response.status_code == 200
    json_data = json.loads(response.data)

    for i, item in enumerate(json_data["opportunities"]):
        assert item == expected_opportunities[i]


@pytest.mark.parametrize(
    "input_data, expected_status",
    [(None, 400), ({"wrong": "wrong"}, 400), ({"id": "not found"}, 404)],
)
def test_user_route_edge_cases(
    test_client: FlaskClient, input_data, expected_status
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET) with various edge case inputs
    THEN check that the response status code is as expected
    """
    response = test_client.get("/user", json=input_data)
    assert response.status_code == expected_status
