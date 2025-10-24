import json

from flask.testing import FlaskClient

from labconnect import db
from labconnect.models import User, UserDepartments, UserMajors


def login_as_student(test_client: FlaskClient):
    """Helper function to log in a user and handle the auth flow."""
    response = test_client.get("/login")
    assert response.status_code == 302

    redirect_url = response.headers["Location"]
    code = redirect_url.split("code=")[1]

    token_response = test_client.post("/token", json={"code": code})
    assert token_response.status_code == 200


# === GET /profile Tests ===


def test_get_profile_success(test_client: FlaskClient):
    """
    logged-in user: '/profile' endpoint is requested (GET)
                    -> correct data and 200 status
    """
    login_as_student(test_client)

    response = test_client.get("/profile")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["email"] == "test@rpi.edu"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert "departments" in data
    assert "majors" in data


def test_get_profile_unauthorized(test_client: FlaskClient):
    """
    no user is logged in: '/profile' endpoint is requested (GET)
                            -> 401 Unauthorized status is returned.
    """
    test_client.get("/logout")
    response = test_client.get("/profile")
    assert response.status_code == 401


# === PUT /profile Tests ===


def test_update_profile_success(test_client: FlaskClient):
    """
    logged-in user: '/profile' endpoint is updated with new data (PUT)
                    -> 200 status and database changed.
    """
    login_as_student(test_client)

    update_data = {
        "first_name": "UpdatedFirst",
        "last_name": "UpdatedLast",
        "preferred_name": "Pref",
        "class_year": 2025,
        "website": "https://new.example.com",
        "description": "This is an updated description.",
        "departments": ["CS"],
        "majors": ["CSCI", "MATH"],
    }

    response = test_client.put("/profile", json=update_data)
    assert response.status_code == 200
    assert "Profile updated successfully" in json.loads(response.data)["msg"]

    # Verify the changes in the database
    user = db.session.execute(
        db.select(User).where(User.email == "test@rpi.edu")
    ).scalar_one()
    assert user.first_name == "UpdatedFirst"
    assert user.website == "https://new.example.com"
    assert user.class_year == 2025

    user_depts = (
        db.session.execute(
            db.select(UserDepartments.department_id).where(
                UserDepartments.user_id == user.id
            )
        )
        .scalars()
        .all()
    )
    assert set(user_depts) == {"CS"}

    user_majors = (
        db.session.execute(
            db.select(UserMajors.major_code).where(UserMajors.user_id == user.id)
        )
        .scalars()
        .all()
    )
    assert set(user_majors) == {"CSCI", "MATH"}


def test_update_profile_partial(test_client: FlaskClient):
    """
    logged-in user: '/profile' endpoint is updated with partial data (PUT)
                    -> check only provided fields updated.
    """
    login_as_student(test_client)

    update_data = {
        "website": "https://partial.update.com",
        "description": "Only this was updated.",
    }

    response = test_client.put("/profile", json=update_data)
    assert response.status_code == 200

    user = db.session.execute(
        db.select(User).where(User.email == "test@rpi.edu")
    ).scalar_one()
    assert user.website == "https://partial.update.com"
    assert user.description == "Only this was updated."
    assert user.last_name == "User"


def test_update_profile_unauthorized(test_client: FlaskClient):
    """
    no user is logged in: '/profile' endpoint is sent a PUT request
                        -> 401 Unauthorized status.
    """
    test_client.get("/logout")
    update_data = {"first_name": "ShouldFail"}
    response = test_client.put("/profile", json=update_data)
    assert response.status_code == 401
