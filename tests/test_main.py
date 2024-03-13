import json

"""
Test mains
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


def test_professor_profile(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorProfile/d1")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data)

    # Test that the "name" key exists
    assert "name" in data
    assert "image" in data
    assert "researchCenter" in data
    assert "department" in data
    assert "description" in data


def test_get_professor_meta(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/getProfessorMeta' endpoint is requested (GET) with valid data
    THEN check that the response is valid and contains expected professor data
    """

    test_data = {
        "user_id": "some_user_id",  # Replace with a valid user ID
        "authToken": "some_auth_token",  # Replace with a valid token
    }

    response = test_client.get(
        "/getProfessorMeta", data=json.dumps(test_data), content_type="application/json"
    )

    assert response.status_code == 200

    data = json.loads(response.data)

    # Assertions on the expected data
    assert "name" in data
    assert "image" in data
    assert "researchCenter" in data
    assert "department" in data
    assert "description" in data
    assert "phone" in data


def test_professor_opportunity_cards(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorOpportunityCards/d1")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))

    # Test that the "name" key exists
    assert len(data.keys()) > 0
    assert "d1" in data.keys()
    print(data)
    for eachCard in data["d1"]:
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "id" in eachCard


def test_get_opportunity(test_client: FlaskClient) -> None:
    response = test_client.get("/getOpportunity/o1")

    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))

    # Test that the "name" key exists
    assert "title" in data
    assert "location" in data
    assert "date" in data
    assert "author" in data
    assert "credits" in data  # and data["credits"] is int
    assert "description" in data  # and data["description"] is str
    assert "salary" in data  # and data["salary"] is int
    assert "upfrontPay" in data  # and data["upfrontPay"] is int
    assert "years" in data  # and data["years"] is list


def test_discover_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/discover' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/discover")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_login_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/login")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_department_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department/<department>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_profile_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/profile/bob")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


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


def test_departments_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/departments' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/departments")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    rpi_departments_data = (
        ("Computer Science", "Biology", "Materials Engineering"),
        ("DS", "life", "also pretty cool"),
    )

    for department in json_data:
        assert department["name"] in rpi_departments_data[0]
        assert department["description"] in rpi_departments_data[1]


def test_majors_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors")

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE", "BIOL", "MATH", "COGS"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
            "Biological Science",
            "Mathematics",
            "Cognitive Science",
        ),
    )

    for major in json_data:
        assert major["major_code"] in majors_data[0]
        assert major["major_name"] in majors_data[1]


def test_years_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/years' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/years")

    assert response.status_code == 200

    assert [2024, 2025, 2026, 2027, 2028, 2029] == json.loads(response.data)
