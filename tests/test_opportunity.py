"""
Test opportunity routes
"""

from flask import json
from flask.testing import FlaskClient


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
