"""
Test opportunity filtering routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient

@pytest.mark.parametrize(
    "filters, expected_opportunities",
    [
        (
            [{"field": "pay", "value": {"min": 14.9, "max": 21}}],
            ["Automated Cooling System"]
        ),
        (
            [{"field": "departments", "value": ["Material Science"]}],
            ["Checking out cubes"]
        ),
        (
            [{"field": "departments", "value": ["Computer Science", "Material Science"]}],
            ["Iphone 15 durability test", "Checking out cubes", "Automated Cooling System"]
        ),
        (
            [{"field": "majors", "value": ["BIOL"]}],
            ["Iphone 15 durability test", "Checking out cubes", "Automated Cooling System"]
        ),
        (
            [{"field": "majors", "value": ["CSCI", "BIOL"]}],
            ["Iphone 15 durability test", "Checking out cubes", "Automated Cooling System"]
        ),
        (
            [{"field": "credits", "value": [1]}],
            ["Iphone 15 durability test", "Checking out cubes"]
        ),
        (
            [{"field": "credits", "value": [2, 4]}],
            ["Iphone 15 durability test", "Checking out cubes", "Automated Cooling System", "Test the water"]
        ),
        (
            [{"field": "class_year", "value": [2025]}],
            ["Iphone 15 durability test"]
        ),
        (
            [{"field": "class_year", "value": [2025, 2027]}],
            ["Iphone 15 durability test", "Automated Cooling System"]
        ),
        (
            [{"field": "location", "value": "Remote"}],
            ["Automated Cooling System"]
        ),
        (
            [{"field": "location", "value": "In-Person"}],
            ["Iphone 15 durability test", "Checking out cubes", "Test the water"]
        ),
        (
            [
                {"field": "location", "value": "In-Person"},
                {"field": "departments", "value": ["Computer Science"]}
            ],
            ["Iphone 15 durability test"]
        ),
        (
            [
                {"field": "credits", "value": [2, 4]},
                {"field": "departments", "value": ["Computer Science"]}
            ],
            ["Iphone 15 durability test", "Automated Cooling System"]
        ),
    ],
)
def test_opportunity_filter(test_client: FlaskClient, filters, expected_opportunities) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/filter' page is requested (GET)
    THEN check that the response is valid
    """
    json_data = {"filters": filters}
    response = test_client.get("/opportunity/filter", json=json_data)

    assert response.status_code == 200

    json_data = json.loads(response.data)

    for data in json_data:
        assert data["name"] in expected_opportunities
