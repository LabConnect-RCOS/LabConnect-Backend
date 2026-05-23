"""
Test staff / lab manager routes with parameterization
"""

import json

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "rcs_id, expected_titles",
    [
        (
            "cenzar",
            {"Automated Cooling System", "Checking out cubes"},
        ),
        (
            "led",
            {"Automated Cooling System", "Iphone 15 durability test"},
        ),
        (
            "turner",
            set(),
        ),
    ],
)
def test_staff_opportunity_cards(
    test_client: FlaskClient, rcs_id: str, expected_titles: set[str]
) -> None:
    response = test_client.get(f"/staff/opportunities/{rcs_id}")
    assert response.status_code == 200

    titles = {card["title"] for card in json.loads(response.data)}
    assert titles == expected_titles


@pytest.mark.parametrize(
    "rcs_id",
    ["missing-user", "notfound99", "xyz"],
)
def test_staff_opportunity_cards_empty(test_client: FlaskClient, rcs_id: str) -> None:
    response = test_client.get(f"/staff/opportunities/{rcs_id}")
    assert response.status_code == 200
    assert json.loads(response.data) == []


@pytest.mark.parametrize(
    "rcs_id, expected_name, expected_department",
    [
        ("cenzar", "Raf Cenzano", "Computer Science"),
        ("led", "Duy Le", "Computer Science"),
        ("holm", "Mark Holmes", "Math"),
    ],
)
def test_staff_profile(
    test_client: FlaskClient,
    auth_headers,
    rcs_id: str,
    expected_name: str,
    expected_department: str,
) -> None:
    response = test_client.get(
        f"/staff/{rcs_id}",
        headers=auth_headers("test@rpi.edu"),
    )
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["name"] == expected_name
    assert data["department"] == expected_department


@pytest.mark.parametrize(
    "rcs_id",
    ["does-not-exist"],
)
def test_staff_profile_not_found(
    test_client: FlaskClient, auth_headers, rcs_id: str
) -> None:
    response = test_client.get(
        f"/staff/{rcs_id}",
        headers=auth_headers("test@rpi.edu"),
    )
    assert response.status_code == 404
