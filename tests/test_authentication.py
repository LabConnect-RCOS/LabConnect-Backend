"""
Test authentication routes
"""

from flask import json
from flask.testing import FlaskClient


def test_login_route_one(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"email": "cenzar@rpi.edu", "password": "testpassworD1"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 200

    assert "access_token" in json.loads(response.data)


def test_login_route_two(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"email": "test@rpi.edu", "password": "testpassworD2"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 200

    assert "access_token" in json.loads(response.data)


def test_login_route_missing_password(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"email": "test@rpi.edu"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 400


def test_login_route_missing_email(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"password": "testpassworD2"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 400


def test_login_route_no_existing_user(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"email": "bob@rpi.edu", "password": "testpassworD2"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 401


def test_login_route_incorrect_password_one(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"email": "cenzar@rpi.edu", "password": "password"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 401

    assert {"msg": "Wrong email or password"} == json.loads(response.data)


def test_login_route_incorrect_password_two(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid
    """

    login_json = {"email": "test@rpi.edu", "password": "testpassword"}
    response = test_client.post("/login", json=login_json)

    assert response.status_code == 401

    assert {"msg": "Wrong email or password"} == json.loads(response.data)
