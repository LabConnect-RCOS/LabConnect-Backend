"""
Test lab manager routes with parameterization
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "input_json, expected_status, expected_response",
    [
        ({"rcs_id": "cenzar"}, 200, {
            "website": None,
            "rcs_id": "cenzar",
            "name": "Rafael",
            "alt_email": None,
            "phone_number": None,
            "email": None,
            "description": None,
        }),
        (None, 400, None),  # No input JSON case
        ({"wrong": "wrong"}, 400, None)  # Incorrect JSON structure case
    ]
)
def test_lab_manager_route(test_client: FlaskClient, input_json, expected_status, expected_response) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET) with different JSON inputs
    THEN check that the response matches the expected outcome
    """
    response = test_client.get("/lab_manager", json=input_json)
    assert response.status_code == expected_status

    if expected_response:
        json_data = json.loads(response.data)
        assert json_data == expected_response


@pytest.mark.parametrize(
    "input_json, expected_status",
    [
        ({"rcs_id": "cenzar"}, 200),
        (None, 400),  # No input JSON case
        ({"wrong": "wrong"}, 400)  # Incorrect JSON structure case
    ]
)
def test_lab_manager_opportunity_cards(test_client: FlaskClient, input_json, expected_status) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET) with different JSON inputs
    THEN check that the response matches the expected status code
    """
    response = test_client.get("/lab_manager/opportunities", json=input_json)
    assert response.status_code == expected_status

    if input_json == {"rcs_id": "cenzar"} and expected_status == 200:
        json_data = json.loads(response.data)
        lab_manager_opportunities_data = [
            {
                "name": "Automated Cooling System",
                "description": "Energy efficient AC system",
                "recommended_experience": "Thermodynamics",
                "pay": 15.0,
                "semester": "Spring",
                "year": 2024,
                "active": True,
            },
            {
                "name": "Iphone 15 durability test",
                "description": "Scratching the Iphone, drop testing etc.",
                "recommended_experience": "Experienced in getting angry and throwing temper tantrum",
                "pay": None,
                "semester": "Spring",
                "year": 2024,
                "active": True,
            },
        ]

        for i, item in enumerate(json_data["cenzar"]):
            assert item["name"] == lab_manager_opportunities_data[i]["name"]
            assert item["description"] == lab_manager_opportunities_data[i]["description"]
            assert item["recommended_experience"] == lab_manager_opportunities_data[i]["recommended_experience"]
            assert item["pay"] == lab_manager_opportunities_data[i]["pay"]
            assert item["semester"] == lab_manager_opportunities_data[i]["semester"]
            assert item["year"] == lab_manager_opportunities_data[i]["year"]
            assert item["active"] == lab_manager_opportunities_data[i]["active"]
