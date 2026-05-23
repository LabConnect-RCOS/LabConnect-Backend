"""
Test opportunity filtering routes
"""

import json

import pytest
from flask.testing import FlaskClient

from tests.conftest import requires_postgres


@requires_postgres
@pytest.mark.parametrize(
    "query_string, expected_opportunities",
    [
        ("hourlypay=14.9", ["Automated Cooling System"]),
        ("majors=BIOL", ["Iphone 15 durability test"]),
        (
            "majors=CSCI,BIOL",
            ["Automated Cooling System", "Iphone 15 durability test"],
        ),
        (
            "credits=1",
            ["Iphone 15 durability test", "Checking out cubes"],
        ),
        (
            "credits=2,4",
            [
                "Iphone 15 durability test",
                "Checking out cubes",
                "Automated Cooling System",
                "Test the water",
            ],
        ),
        ("years=2025", ["Iphone 15 durability test", "Checking out cubes"]),
        (
            "years=2025,2027",
            [
                "Iphone 15 durability test",
                "Checking out cubes",
                "Automated Cooling System",
            ],
        ),
        ("location=Remote", ["Automated Cooling System"]),
        (
            "location=In-Person",
            [
                "Iphone 15 durability test",
                "Checking out cubes",
                "Test the water",
                "Data Science Research",
            ],
        ),
        (
            "location=In-Person&departments=CSCI",
            ["Iphone 15 durability test", "Automated Cooling System"],
        ),
        (
            "credits=2,4&departments=CSCI",
            ["Iphone 15 durability test", "Automated Cooling System"],
        ),
        ("departments=MTLE", ["Test the water"]),
        (
            "departments=CSCI,MTLE",
            [
                "Automated Cooling System",
                "Iphone 15 durability test",
                "Test the water",
            ],
        ),
    ],
)
def test_opportunity_filter(
    test_client: FlaskClient,
    auth_headers,
    query_string,
    expected_opportunities,
) -> None:
    response = test_client.get(
        f"/opportunity/filter?{query_string}",
        headers=auth_headers("test@rpi.edu"),
    )
    assert response.status_code == 200

    names = {item["name"] for item in json.loads(response.data)}
    for expected in expected_opportunities:
        assert expected in names


@requires_postgres
@pytest.mark.parametrize(
    "query_string, expected_status",
    [
        ("years=not-a-year", 400),
        ("credits=9", 400),
        ("unknown=value", 400),
    ],
)
def test_opportunity_filter_invalid_params(
    test_client: FlaskClient, auth_headers, query_string, expected_status
) -> None:
    response = test_client.get(
        f"/opportunity/filter?{query_string}",
        headers=auth_headers("test@rpi.edu"),
    )
    assert response.status_code == expected_status


def test_opportunity_filter_requires_auth(test_client: FlaskClient) -> None:
    response = test_client.get("/opportunity/filter")
    assert response.status_code == 401
