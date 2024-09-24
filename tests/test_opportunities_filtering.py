"""
Test opportunity filtering routes
"""

from flask import json
from flask.testing import FlaskClient


def test_opportunity_filter_pay(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "pay", "value": {"min": 14.9, "max": 21}}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert "Automated Cooling System" == json_data[0]["name"]


def test_opportunity_filter_department(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "departments", "value": ["Material Science"]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert "Checking out cubes" == json_data[0]["name"]


def test_opportunity_filter_departments(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {
        "filters": [
            {"field": "departments", "value": ["Computer Science", "Material Science"]}
        ]
    }
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Checking out cubes",
        "Automated Cooling System",
    )

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_major(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "majors", "value": ["BIOL"]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Checking out cubes",
        "Automated Cooling System",
    )

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_majors(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "majors", "value": ["CSCI", "BIOL"]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Checking out cubes",
        "Automated Cooling System",
    )

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_credits(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "credits", "value": [1]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Checking out cubes",
    )

    for data in json_data:
        assert data["name"] in opportunities

    json_data = {"filters": [{"field": "credits", "value": [2, 4]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Checking out cubes",
        "Automated Cooling System",
        "Test the water",
    )

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_class_years(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "class_year", "value": [2025]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = ("Iphone 15 durability test",)

    for data in json_data:
        assert data["name"] in opportunities

    json_data = {"filters": [{"field": "class_year", "value": [2025, 2027]}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Automated Cooling System",
    )

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_location_remote(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "location", "value": "Remote"}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert "Automated Cooling System" == json_data[0]["name"]


def test_opportunity_filter_location_in_person(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {"filters": [{"field": "location", "value": "In-Person"}]}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = (
        "Iphone 15 durability test",
        "Checking out cubes",
        "Test the water",
    )

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_location_departments(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {
        "filters": [
            {"field": "location", "value": "In-Person"},
            {"field": "departments", "value": ["Computer Science"]},
        ]
    }
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = ("Iphone 15 durability test",)

    for data in json_data:
        assert data["name"] in opportunities


def test_opportunity_filter_credits_departments(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """

    json_data = {
        "filters": [
            {"field": "credits", "value": [2, 4]},
            {"field": "departments", "value": ["Computer Science"]},
        ]
    }
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    opportunities = ("Iphone 15 durability test", "Automated Cooling System")

    for data in json_data:
        assert data["name"] in opportunities


# TODO: Add test for no fields
