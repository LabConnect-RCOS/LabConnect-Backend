"""
Test user routes
"""

from flask import json
from flask.testing import FlaskClient


def test_user_route_with_input_id_1(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user", json={"id": "1"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert json_data["id"] == 1
    assert json_data["first_name"] == "Rafael"
    assert json_data["preferred_name"] == "Raf"
    assert json_data["last_name"] == "Cenzano"
    assert json_data["email"] == "cenzar@rpi.edu"
    #Added
    assert json_data["description"] == "labconnect is the best RCOS project"
    assert json_data["profile_picture"] == "https://rafael.sirv.com/Images/rafael.jpeg?thumbnail=350&format=webp&q=90"
    assert json_data["website"] == "https://rafaelcenzano.com"
    #class year
    assert json_data["class_year"] == "2025"
    #lab manager id
    assert json_data["lab_manager_id"] == 1

    departments_data = [
        {"user_id": 1, "department_id": "Computer Science"},
        {"user_id": 1, "department_id": "Math"},
    ]

    major_data = [
        {"user_id": 1, "major_code": "CSCI"},
        {"user_id": 1, "major_code": "MATH"},
    ]

    course_data = [
        {"in_progress": False, "user_id": 1, "course_code": "CSCI2300"},
        {"in_progress": True, "user_id": 1, "course_code": "CSCI4430"},
    ]

    assert json_data["departments"] == departments_data
    assert json_data["majors"] == major_data
    assert json_data["courses"] == course_data


def test_user_1_opportunity_cards(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user", json={"id": 1})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    lab_manager_opportunities_data = (
        (
            "Automated Cooling System",
            "Energy efficient AC system",
            "Thermodynamics",
            15.0,
            "Spring",
            2024,
            True,
        ),
        (
            "Iphone 15 durability test",
            "Scratching the Iphone, drop testing etc.",
            "Experienced in getting angry and throwing temper tantrum",
            None,
            "Spring",
            2024,
            True,
        ),
    )

    for i, item in enumerate(json_data["opportunities"]):
        assert item["name"] == lab_manager_opportunities_data[i][0]
        assert item["description"] == lab_manager_opportunities_data[i][1]
        assert item["recommended_experience"] == lab_manager_opportunities_data[i][2]
        assert item["pay"] == lab_manager_opportunities_data[i][3]
        assert item["semester"] == lab_manager_opportunities_data[i][4]
        assert item["year"] == lab_manager_opportunities_data[i][5]
        assert item["active"] == lab_manager_opportunities_data[i][6]


def test_user_route_with_input_id_2(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user", json={"id": 2})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert json_data["id"] == 2
    assert json_data["first_name"] == "RCOS"
    assert json_data["last_name"] == "RCOS"
    assert json_data["preferred_name"] is None
    assert json_data["email"] == "test@rpi.edu"
    #Added 
    assert json_data["description"] is None  
    assert json_data["profile_picture"] == "https://www.svgrepo.com/show/206842/professor.svg"  # Adjust based on your test data
    assert json_data["website"] is None 
    assert json_data["class_year"] is None
    assert json_data["lab_manager_id"] is None

    departments_data = [
        {"department_id": "Computer Science", "user_id": 2},
    ]

    major_data = [
        {"user_id": 2, "major_code": "CSCI"},
    ]

    course_data = [
        {"in_progress": False, "user_id": 2, "course_code": "CSCI2300"},
    ]

    assert json_data["departments"] == departments_data
    assert json_data["majors"] == major_data
    assert json_data["courses"] == course_data


def test_user_2_opportunity_cards(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user", json={"id": 2})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    lab_manager_opportunities_data = (
        (
            "Checking out cubes",
            "Material Sciences",
            "Experienced in materials.",
            None,
            "Fall",
            2024,
            True,
        ),
        (
            "Test the water",
            "Testing the quality of water in Troy pipes",
            "Understanding of lead poisioning",
            None,
            "Summer",
            2024,
            True,
        ),
    )

    for i, item in enumerate(json_data["opportunities"]):
        assert item["name"] == lab_manager_opportunities_data[i][0]
        assert item["description"] == lab_manager_opportunities_data[i][1]
        assert item["recommended_experience"] == lab_manager_opportunities_data[i][2]
        assert item["pay"] == lab_manager_opportunities_data[i][3]
        assert item["semester"] == lab_manager_opportunities_data[i][4]
        assert item["year"] == lab_manager_opportunities_data[i][5]
        assert item["active"] == lab_manager_opportunities_data[i][6]


def test_user_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user")

    assert response.status_code == 400


def test_user_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user", json={"wrong": "wrong"})

    assert response.status_code == 400


def test_user_not_found(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/user", json={"id": "not found"})

    print(json.loads(response.data))

    assert response.status_code == 404
