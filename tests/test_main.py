import json

"""
Test mains
"""

from flask import json
from flask.testing import FlaskClient
import json

from labconnect.helpers import SemesterEnum


def test_home_page(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")

    assert response.status_code == 200

    assert {"Hello": "There"} == json.loads(response.data)


def test_professor_opportunity_cards(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager/opportunities", json={"rcs_id": "cenzar"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    lab_manager_opportunities_data = (
        (
            "Automated Cooling System",
            "Energy efficient AC system",
            "Thermodynamics",
            15.0,
            "4",
            "Spring",
            2024,
            True,
        ),
        (
            "Iphone 15 durability test",
            "Scratching the Iphone, drop testing etc.",
            "Experienced in getting angry and throwing temper tantrum",
            None,
            "1,2,3,4",
            "Spring",
            2024,
            True,
        ),
    )

    for i, item in enumerate(json_data["cenzar"]):
        assert item["name"] == lab_manager_opportunities_data[i][0]
        assert item["description"] == lab_manager_opportunities_data[i][1]
        assert item["recommended_experience"] == lab_manager_opportunities_data[i][2]
        assert item["pay"] == lab_manager_opportunities_data[i][3]
        assert item["credits"] == lab_manager_opportunities_data[i][4]
        assert item["semester"] == lab_manager_opportunities_data[i][5]
        assert item["year"] == lab_manager_opportunities_data[i][6]
        assert item["active"] == lab_manager_opportunities_data[i][7]


def test_professor_opportunity_cards_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager/opportunities")

    assert response.status_code == 400


def test_professor_opportunity_cards_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager/opportunities", json={"wrong": "wrong"})

    assert response.status_code == 400


def test_get_opportunity(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET)
    THEN check that the response is valid
    """
    response1 = test_client.get("/opportunity", json={"id": 1})
    response2 = test_client.get("/opportunity", json={"id": 2})

    assert response1.status_code == 200
    assert response2.status_code == 200

    json_data1 = json.loads(response1.data)
    json_data2 = json.loads(response2.data)

    lab_manager_opportunities_data = (
        (
            "Automated Cooling System",
            "Energy efficient AC system",
            "Thermodynamics",
            15.0,
            "4",
            "Spring",
            2024,
            True,
        ),
        (
            "Iphone 15 durability test",
            "Scratching the Iphone, drop testing etc.",
            "Experienced in getting angry and throwing temper tantrum",
            None,
            "1,2,3,4",
            "Spring",
            2024,
            True,
        ),
    )

    assert json_data1["name"] == lab_manager_opportunities_data[0][0]
    assert json_data1["description"] == lab_manager_opportunities_data[0][1]
    assert json_data1["recommended_experience"] == lab_manager_opportunities_data[0][2]
    assert json_data1["pay"] == lab_manager_opportunities_data[0][3]
    assert json_data1["credits"] == lab_manager_opportunities_data[0][4]
    assert json_data1["semester"] == lab_manager_opportunities_data[0][5]
    assert json_data1["year"] == lab_manager_opportunities_data[0][6]
    assert json_data1["active"] == lab_manager_opportunities_data[0][7]

    assert json_data2["name"] == lab_manager_opportunities_data[1][0]
    assert json_data2["description"] == lab_manager_opportunities_data[1][1]
    assert json_data2["recommended_experience"] == lab_manager_opportunities_data[1][2]
    assert json_data2["pay"] == lab_manager_opportunities_data[1][3]
    assert json_data2["credits"] == lab_manager_opportunities_data[1][4]
    assert json_data2["semester"] == lab_manager_opportunities_data[1][5]
    assert json_data2["year"] == lab_manager_opportunities_data[1][6]
    assert json_data2["active"] == lab_manager_opportunities_data[1][7]


def test_get_opportunity_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/opportunity")

    assert response.status_code == 400


def test_opportunity_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/opportunity", json={"wrong": "wrong"})

    assert response.status_code == 400


def test_discover_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/discover' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/discover")
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert data["data"][0] == {
        "title": "Nelson",
        "major": "CS",
        "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
        "credits": 4,
        "pay": 9000.0,
    }


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
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json={"department": "Computer Science"})

    assert response.status_code == 200

    assert {"name": "Computer Science", "description": "DS"} == json.loads(
        response.data
    )


def test_department_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department")

    assert response.status_code == 400


def test_department_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department", json={"wrong": "wrong"})

    assert response.status_code == 400


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
        assert major["code"] in majors_data[0]
        assert major["name"] in majors_data[1]


def test_majors_route_with_input_name(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json={"input": "computer"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
        ),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == majors_data[0][i]
        assert major["name"] == majors_data[1][i]


def test_majors_route_with_input_code(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/majors", json={"input": "cs"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    majors_data = (
        ("CSCI", "ECSE", "MATH"),
        (
            "Computer Science",
            "Electrical, Computer, and Systems Engineering",
            "Mathematics",
        ),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == majors_data[0][i]
        assert major["name"] == majors_data[1][i]


def test_years_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/years' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/years")

    assert response.status_code == 200

    assert [2024, 2025, 2026, 2027, 2028, 2029] == json.loads(response.data)


def test_courses_route_with_input_name(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"input": "data"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    print(json_data)

    assert json_data[0]["code"] == "CSCI4390"
    assert json_data[0]["name"] == "Data Mining"


def test_courses_route_with_input_code(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"input": "cs"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    course_data = (
        ("CSCI2961", "CSCI4390", "CSCI4430"),
        ("Rensselaer Center for Open Source", "Data Mining", "Programming Languages"),
    )

    for i, major in enumerate(json_data):
        assert major["code"] == course_data[0][i]
        assert major["name"] == course_data[1][i]


def test_courses_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses")

    assert response.status_code == 400


def test_courses_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/courses' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/courses", json={"wrong": "wrong"})

    assert response.status_code == 400


def test_lab_manager_route_with_input_id(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager", json={"rcs_id": "cenzar"})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    cenzar_data = {
        "website": None,
        "rcs_id": "cenzar",
        "name": "Rafael",
        "alt_email": None,
        "phone_number": None,
        "email": None,
    }

    assert json_data == cenzar_data


def test_lab_manager_route_no_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager")

    assert response.status_code == 400


def test_lab_manager_route_incorrect_json(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/lab_manager", json={"wrong": "wrong"})

    assert response.status_code == 400
