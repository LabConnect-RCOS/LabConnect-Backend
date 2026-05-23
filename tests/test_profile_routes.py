import json

import pytest
from flask.testing import FlaskClient

from labconnect import db
from labconnect.models import User, UserDepartments, UserMajors


@pytest.fixture(autouse=True)
def restore_test_user(test_client):
    """Reset test@rpi.edu after profile write tests so
    other modules stay deterministic."""
    yield
    with test_client.application.app_context():
        user = db.session.get(User, "test")
        if user is None:
            return
        user.first_name = "RCOS"
        user.last_name = "RCOS"
        user.preferred_name = None
        user.class_year = None
        user.website = None
        user.description = "first test"
        db.session.execute(
            db.delete(UserDepartments).where(UserDepartments.user_id == user.id)
        )
        db.session.execute(db.delete(UserMajors).where(UserMajors.user_id == user.id))
        db.session.add(UserDepartments(user_id=user.id, department_id="CSCI"))
        db.session.add(UserMajors(user_id=user.id, major_code="CSCI"))
        db.session.commit()


def test_get_profile_success(test_client: FlaskClient, login_as_test_user):
    response = test_client.get("/profile", headers=login_as_test_user)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["email"] == "test@rpi.edu"
    assert data["first_name"] == "RCOS"
    assert data["last_name"] == "RCOS"
    assert "departments" in data
    assert "majors" in data


def test_get_profile_unauthorized(test_client: FlaskClient):
    response = test_client.get("/profile")
    assert response.status_code == 401


def test_update_profile_success(test_client: FlaskClient, login_as_test_user):
    update_data = {
        "first_name": "UpdatedFirst",
        "last_name": "UpdatedLast",
        "preferred_name": "Pref",
        "class_year": 2025,
        "website": "https://new.example.com",
        "description": "This is an updated description.",
        "departments": ["CSCI"],
        "majors": ["CSCI", "MATH"],
    }

    response = test_client.put("/profile", headers=login_as_test_user, json=update_data)
    assert response.status_code == 200
    assert "Profile updated successfully" in json.loads(response.data)["msg"]

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
    assert set(user_depts) == {"CSCI"}

    user_majors = (
        db.session.execute(
            db.select(UserMajors.major_code).where(UserMajors.user_id == user.id)
        )
        .scalars()
        .all()
    )
    assert set(user_majors) == {"CSCI", "MATH"}


def test_update_profile_partial(test_client: FlaskClient, login_as_test_user):
    update_data = {
        "website": "https://partial.update.com",
        "description": "Only this was updated.",
    }

    response = test_client.put("/profile", headers=login_as_test_user, json=update_data)
    assert response.status_code == 200

    user = db.session.execute(
        db.select(User).where(User.email == "test@rpi.edu")
    ).scalar_one()
    assert user.website == "https://partial.update.com"
    assert user.description == "Only this was updated."


def test_update_profile_unauthorized(test_client: FlaskClient):
    response = test_client.put("/profile", json={"first_name": "ShouldFail"})
    assert response.status_code == 401
