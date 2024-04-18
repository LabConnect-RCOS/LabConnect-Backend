from flask import json
from flask.testing import FlaskClient

def test_majors_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET) without any input
    THEN check that the response is valid and contains all majors
    """
    # WHEN
    response = test_client.get("/majors")

    # THEN
    assert response.status_code == 200
    json_data = json.loads(response.data)
    expected_majors = {
        "CSCI": "Computer Science",
        "ECSE": "Electrical, Computer, and Systems Engineering",
        "BIOL": "Biological Science",
        "MATH": "Mathematics",
        "COGS": "Cognitive Science",
    }
    for major in json_data:
        assert major["code"] in expected_majors
        assert major["name"] == expected_majors[major["code"]]

def test_majors_route_with_input(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/majors' page is requested (GET) with input provided
    THEN check that the response is valid and contains filtered majors
    """
    # WHEN
    response = test_client.get("/majors", query_string={"input": "cs"})

    # THEN
    assert response.status_code == 200
    json_data = json.loads(response.data)
    expected_majors = {
        "CSCI": "Computer Science",
        "ECSE": "Electrical, Computer, and Systems Engineering",
        "MATH": "Mathematics",
    }
    for major in json_data:
        assert major["code"] in expected_majors
        assert major["name"] == expected_majors[major["code"]]
