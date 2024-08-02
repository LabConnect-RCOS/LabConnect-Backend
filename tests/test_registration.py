"""
Test registration routes
"""

# from flask import json
# from flask.testing import FlaskClient


# def test_register_route(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "password": "testpassworDMarty",
#         "first_name": "Martin",
#         "last_name": "Schmidt",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 200

#     assert {"msg": "User created successfully"} == json.loads(response.data)


# def test_register_route_with_same_data(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "password": "testpassworDMarty",
#         "first_name": "Martin",
#         "last_name": "Schmidt",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 403

#     assert {"msg": "User already exists"} == json.loads(response.data)


# def test_register_route_with_preferred_name(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "martin@rpi.edu",
#         "password": "testpassworDMarty",
#         "first_name": "Martin",
#         "last_name": "Schmidt",
#         "preferred_name": "Marty",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 200

#     assert {"msg": "User created successfully"} == json.loads(response.data)


# def test_register_route_with_same_email_different_data(
#     test_client: FlaskClient,
# ) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "password": "testpassasdsuaworDMarty",
#         "first_name": "Martin",
#         "last_name": "Schmidt II",
#         "class_year": 2024,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 403

#     assert {"msg": "User already exists"} == json.loads(response.data)


# def test_register_route_missing_class_year(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "password": "testpassworDMarty",
#         "first_name": "Martin",
#         "last_name": "Schmidt",
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 400


# def test_register_route_missing_first_name(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "password": "testpassworDMarty",
#         "last_name": "Schmidt",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 400


# def test_register_route_missing_last_name(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "password": "testpassworDMarty",
#         "first_name": "Martin",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 400


# def test_register_route_missing_password(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "email": "marty@rpi.edu",
#         "first_name": "Martin",
#         "last_name": "Schmidt",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 400


# def test_register_route_missing_email(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {
#         "password": "testpassworDMarty",
#         "first_name": "Martin",
#         "last_name": "Schmidt",
#         "class_year": 2023,
#     }
#     response = test_client.post("/register", json=login_json)

#     assert response.status_code == 400


# def test_register_route_no_data(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' route is requested (POST)
#     THEN check that the response is valid
#     """

#     response = test_client.post("/register")

#     assert response.status_code == 400
