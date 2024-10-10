"""
Test general routes
"""

from flask import json
from flask.testing import FlaskClient
import pytest


def test_home_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")

    assert response.status_code == 200
    assert {"Hello": "There"} == json.loads(response.data)


def test_discover_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/discover' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/discover")

    assert response.status_code == 200
    # Uncomment and modify the following line with expected response data
    # data = json.loads(response.data.decode("utf-8"))
    # assert data["data"][0] == {
    #     "title": "Nelson",
    #     "major": "CS",
    #     "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
    #     "pay": 9000.0,
    # }


@pytest.mark.parametrize(
    "input_id, expected_profile",
    [
        (1, {
            "id": "cenzar",
            "first_name": "Rafael",
            "opportunities": [ ... ]  # Replace with expected opportunities data
        })
    ],
)
def test_profile_page(test_client: FlaskClient, input_id, expected_profile) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/profile", json={"id": input_id})

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
    assert [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031] == json.loads(response.data)


def test_professor_profile(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/getProfessorProfile/<id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/getProfessorProfile/1")
    
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
