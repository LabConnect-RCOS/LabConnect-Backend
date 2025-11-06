"""
Test authentication routes
"""

from flask import json
from flask.testing import FlaskClient
import pytest


# def test_login_route_one(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "cenzar@rpi.edu", "password": "testpassworD1"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 200

#     assert "access_token" in json.loads(response.data)


# def test_login_route_two(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "test@rpi.edu", "password": "testpassworD2"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 200

#     assert "access_token" in json.loads(response.data)


# def test_login_route_missing_password(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "test@rpi.edu"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 400


# def test_login_route_missing_email(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"password": "testpassworD2"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 400


# def test_login_route_no_existing_user(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "bob@rpi.edu", "password": "testpassworD2"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 401


# def test_login_route_incorrect_password_one(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "cenzar@rpi.edu", "password": "password"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 401

#     assert {"msg": "Wrong email or password"} == json.loads(response.data)


# def test_login_route_incorrect_password_two(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "test@rpi.edu", "password": "testpassword"}
#     response = test_client.post("/login", json=login_json)

#     assert response.status_code == 401

#     assert {"msg": "Wrong email or password"} == json.loads(response.data)


# def test_logout_route_one(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     WHEN the '/logout' route is requested (GET)
#     THEN check that the responde is valid
#     """

#     login_json = {"email": "cenzar@rpi.edu", "password": "testpassworD1"}
#     response_login = test_client.post("/login", json=login_json)

#     assert response_login.status_code == 200

#     assert "access_token" in json.loads(response_login.data)

#     response_logout = test_client.get("/logout")

#     assert response_logout.status_code == 200

#     assert {"msg": "logout successful"} == json.loads(response_logout.data)


# def test_logout_route_two(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     login_json = {"email": "test@rpi.edu", "password": "testpassworD2"}
#     response_login = test_client.post("/login", json=login_json)

#     assert response_login.status_code == 200

#     assert "access_token" in json.loads(response_login.data)

#     response_logout = test_client.get("/logout")

#     assert response_logout.status_code == 200

#     assert {"msg": "logout successful"} == json.loads(response_logout.data)


# def test_login_route_no_data(test_client: FlaskClient) -> None:
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' route is requested (POST)
#     THEN check that the response is valid
#     """

#     response = test_client.post("/login")

#     assert response.status_code == 400

"""
Test Lab Manager promotion route (/users/<string:email>/permissions)
"""

@pytest.mark.parametrize(
    "rcsid, client_fixture, expected_status, expected_msg",
    [
        # Scenario 1: Successful Promotion by Super Admin
        (
            "target_rcsid@rpi.edu",  # Target user exists and is ready to be promoted
            "super_admin_client",
            200,
            "User promoted to Lab Manager",
        ),
        # Scenario 2: Promotion Attempt by Non-Admin/Student (Permission Failure)
        (
            "target_rcsid@rpi.edu",
            "student_client",  # Client lacks super_admin=True
            401,
            "Missing permissions",
        ),
        # Scenario 3: Target User Not Found
        (
            "non_existent_rcsid@rpi.edu",  # User does not exist in the DB
            "super_admin_client",
            500,  # Based on your route returning 500 for 'No user matches RCS ID'
            "No user matches RCS ID",
        ),
    ],
)
def test_promote_user_permissions(
    rcsid: str,
    client_fixture: str,
    expected_status: int,
    expected_msg: str,
    request, # Used to dynamically access the client fixture
    db, # Used for pre-test setup and post-test verification
) -> None:
    """
    GIVEN a Flask application and various authenticated test clients
    WHEN a PATCH request is made to the /users/<rcsid>/permissions endpoint
    THEN check that the response status and the user's permissions are updated correctly.
    """
    # Dynamically retrieve the correct test client fixture (super_admin_client or student_client)
    test_client: FlaskClient = request.getfixturevalue(client_fixture)
    
    # 1. SETUP: Ensure a target user exists if we are testing promotion/permission issues
    # NOTE: You must implement a fixture that creates the users (e.g., target_rcsid@rpi.edu)
    #       before this test runs, otherwise the target user won't exist in the DB.
    # We will assume 'setup_users' fixture handles this.

    # 2. ACT: Send the PATCH request
    endpoint = f"/users/{rcsid}/permissions"
    response = test_client.patch(
        endpoint, 
        json={"is_admin": True} # Payload doesn't matter much here, but should be included
    )
    
    # 3. ASSERT: Check Status Code and Response Message
    assert response.status_code == expected_status
    json_data = json.loads(response.data)
    assert json_data.get("msg") == expected_msg
    
    # 4. ASSERT (Conditional): Check Database state for successful promotion
    if expected_status == 200:
        # Find the target user in the DB
        User = db.get_model('User') # Assuming a helper function to get model classes
        ManagementPermissions = db.get_model('ManagementPermissions')

        promoted_user = db.session.query(User).filter_by(email=rcsid).one_or_none()
        
        # Ensure the user was found and promoted
        assert promoted_user is not None
        
        # Check the ManagementPermissions record for the promoted user
        perms = db.session.query(ManagementPermissions).filter_by(user_id=promoted_user.id).one_or_none()
        
        # The permission should be True after a successful promotion
        assert perms is not None
        assert perms.admin is True
        # Ensure super_admin wasn't accidentally set (assuming promotion only sets 'admin')
        assert perms.super_admin is False

