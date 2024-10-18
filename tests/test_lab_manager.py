"""
Test lab manager routes
"""

from flask import json
from flask.testing import FlaskClient
import pytest


@pytest.mark.parametrize(
    "json_data, expected_status, expected_response",
    [
        (
            {"rcs_id": "cenzar"},
            200,
            {
                "website": None,
                "rcs_id": "cenzar",
                "name": "Rafael",
                "alt_email": None,
                "phone_number": None,
                "email": None,
            },
        ),
        (None, 400, None),
        ({"wrong": "wrong"}, 400, None),
    ],
)
def test_lab_manager_route(test_client: FlaskClient, json_data, expected_status, expected_response) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager' page is requested (GET)
    THEN check that the response status and data are as expected
    """
    response = test_client.get("/lab_manager", json=json_data)

    assert response.status_code == expected_status

    if expected_response is not None:
        json_response = json.loads(response.data)
        assert json_response == expected_response


@pytest.mark.parametrize(
    "json_data, expected_status, expected_opportunities",
    [
        (
            {"rcs_id": "cenzar"},
            200,
            [
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
            ],
        ),
        (None, 400, None),
        ({"wrong": "wrong"}, 400, None),
    ],
)
def test_lab_manager_opportunity_cards(test_client: FlaskClient, json_data, expected_status, expected_opportunities) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/lab_manager/opportunities' page is requested (GET)
    THEN check that the response status and data are as expected
    """
    response = test_client.get("/lab_manager/opportunities", json=json_data)

    assert response.status_code == expected_status

    if expected_opportunities is not None:
        json_response = json.loads(response.data)
        for i, item in enumerate(json_response["cenzar"]):
            assert item["name"] == expected_opportunities[i][0]
            assert item["description"] == expected_opportunities[i][1]
            assert item["recommended_experience"] == expected_opportunities[i][2]
            assert item["pay"] == expected_opportunities[i][3]
            assert item["semester"] == expected_opportunities[i][4]
            assert item["year"] == expected_opportunities[i][5]
            assert item["active"] == expected_opportunities[i][6]
