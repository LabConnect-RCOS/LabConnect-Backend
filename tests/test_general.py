"""
Test general routes
"""

from flask import json
from flask.testing import FlaskClient


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
    # data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    # print(data)
    # assert data["data"][0] == {
    #     "title": "Nelson",
    #     "major": "CS",
    #     "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
    #     "pay": 9000.0,
    # }


def test_profile_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/profile", json={"rcs_id": "cenzar"})

    assert response.status_code == 200

    json_data = json.loads(response.data)
    assert json_data["rcs_id"] == "cenzar"
    assert json_data["name"] == "Rafael"
    assert json_data["opportunities"] != []


def test_schools_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/schools' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/schools")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    rpi_schools_data = (
        ("School of Science", "School of Engineering"),
        ("the coolest of them all", "also pretty cool"),
    )

    for school in json_data:
        assert school["name"] in rpi_schools_data[0]
        assert school["description"] in rpi_schools_data[1]


def test_years_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/years' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/years")

    assert response.status_code == 200

    assert [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031] == json.loads(response.data)
