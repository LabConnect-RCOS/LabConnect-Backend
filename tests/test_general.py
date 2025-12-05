"""
Test general routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token


def test_home_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")

    assert response.status_code == 200
    assert {"Hello": "There"} == json.loads(response.data)


@pytest.mark.parametrize(
    "input_id, expected_profile",
    [
        (
            1,
            {
                "id": "cenzar",
                "first_name": "Rafael",
                "opportunities": ["opportunity1"],  
                # Replace with expected opportunities data
            },
        )
    ],
)
def test_profile_page(test_client: FlaskClient, input_id, expected_profile) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    # login_response = test_client.post("/login", 
    # json={"username": "test_user", "password": "password123"})
    # login_data = json.loads(login_response.data)
    with test_client.application.app_context():
        access_token = create_access_token(identity='cenzar@rpi.edu')

    # response = test_client.get("/profile", json={"id": input_id})
    # Make the request with the JWT token
    response = test_client.get(
        "/profile",
        json={"id": input_id},
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200

    json_data = json.loads(response.data)
    assert json_data["id"] == expected_profile["id"]
    assert json_data["first_name"] == expected_profile["first_name"]
    assert json_data["opportunities"] != []


@pytest.mark.parametrize(
    "expected_schools",
    [
        (
            (
                "School of Science",
                "School of Engineering",
            ),
            (
                "the coolest of them all",
                "also pretty cool",
            ),
        )
    ],
)
def test_schools_route(test_client: FlaskClient, expected_schools) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/schools' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/schools")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for school in json_data:
        assert school["name"] in expected_schools[0]
        assert school["description"] in expected_schools[1]


def test_years_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/years' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/years")

    assert response.status_code == 200
    assert [2025, 2026, 2027, 2028, 2029, 2030, 2031] == json.loads(response.data)


def test_professor_profile(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/getProfessorProfile/<id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/staff/cenzar")

    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data)

    assert data["first_name"] == "Rafael"
    assert data["last_name"] == "Cenzano"
    assert data["preferred_name"] == "Raf"
    assert data["email"] == "cenzar@rpi.edu"
    assert data["department_id"] == "Computer Science"
    assert data["id"] == "cenzar"
    assert "phone_number" in data
    assert "website" in data
