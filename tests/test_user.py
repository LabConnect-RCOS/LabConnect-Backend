"""
Test user/profile routes (replaces legacy /user JSON endpoints).
"""

import json

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "email, expected_profile",
    [
        (
            "cenzar@rpi.edu",
            {
                "id": "cenzar",
                "first_name": "Rafael",
                "preferred_name": "Raf",
                "last_name": "Cenzano",
                "email": "cenzar@rpi.edu",
                "class_year": 2025,
                "majors": ["CSCI", "MATH"],
                "departments": ["CSCI", "MATH"],
            },
        ),
        (
            "test@rpi.edu",
            {
                "id": "test",
                "first_name": "RCOS",
                "preferred_name": None,
                "last_name": "RCOS",
                "email": "test@rpi.edu",
                "majors": ["CSCI"],
                "departments": ["CSCI"],
            },
        ),
    ],
)
def test_profile_route(
    test_client: FlaskClient, auth_headers, email, expected_profile
) -> None:
    response = test_client.get("/profile", headers=auth_headers(email))
    assert response.status_code == 200

    data = json.loads(response.data)
    for key, value in expected_profile.items():
        assert data[key] == value


@pytest.mark.parametrize(
    "rcs_id, expected_titles",
    [
        (
            "cenzar",
            ["Automated Cooling System", "Iphone 15 durability test"],
        ),
        (
            "test",
            ["Checking out cubes", "Test the water"],
        ),
    ],
)
def test_profile_opportunity_cards(
    test_client: FlaskClient,
    auth_headers,
    rcs_id: str,
    expected_titles: list[str],
) -> None:
    response = test_client.get(
        f"/profile/opportunities/{rcs_id}",
        headers=auth_headers("test@rpi.edu"),
    )
    assert response.status_code == 200

    titles = {card["title"] for card in json.loads(response.data)}
    assert titles == set(expected_titles)


@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("/profile", 401),
    ],
)
def test_profile_route_edge_cases(
    test_client: FlaskClient, endpoint, expected_status
) -> None:
    response = test_client.get(endpoint)
    assert response.status_code == expected_status
