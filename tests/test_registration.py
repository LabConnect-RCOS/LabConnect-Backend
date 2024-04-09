"""
Test registration routes
"""

from flask import json
from flask.testing import FlaskClient


def test_register_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "email": "marty@rpi.edu",
        "password": "testpassworDMarty",
        "name": "Martin Schmidt",
        "class_year": 2023,
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 200

    assert {"msg": "User created successfully"} == json.loads(response.data)


def test_register_route_with_same_data(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "email": "marty@rpi.edu",
        "password": "testpassworDMarty",
        "name": "Martin Schmidt",
        "class_year": 2023,
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 403

    assert {"msg": "User already exists"} == json.loads(response.data)


def test_register_route_with_same_email_different_data(
    test_client: FlaskClient,
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "email": "marty@rpi.edu",
        "password": "testpassasdsuaworDMarty",
        "name": "Martin Schmidt II",
        "class_year": 2024,
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 403

    assert {"msg": "User already exists"} == json.loads(response.data)


def test_register_route_missing_class_year(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "email": "marty@rpi.edu",
        "password": "testpassworDMarty",
        "name": "Martin Schmidt",
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 400


def test_register_route_missing_name(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "email": "marty@rpi.edu",
        "password": "testpassworDMarty",
        "class_year": 2023,
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 400


def test_register_route_missing_password(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "email": "marty@rpi.edu",
        "name": "Martin Schmidt",
        "class_year": 2023,
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 400


def test_register_route_missing_email(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {
        "password": "testpassworDMarty",
        "name": "Martin Schmidt",
        "class_year": 2023,
    }
    response = test_client.post("/register", json=login_json)

    assert response.status_code == 400


def test_register_route_no_data(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid
    """

    response = test_client.post("/register")

    assert response.status_code == 400
