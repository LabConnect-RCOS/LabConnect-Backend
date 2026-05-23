"""
Test general routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "route, expected_body",
    [
        ("/", {"Hello": "There"}),
    ],
)
def test_static_routes(
    test_client: FlaskClient, route: str, expected_body: dict
) -> None:
    response = test_client.get(route)
    assert response.status_code == 200
    assert json.loads(response.data) == expected_body


@pytest.mark.parametrize(
    "expected_years",
    [
        ([2025, 2026, 2027, 2028, 2029, 2030, 2031],),
    ],
)
def test_years_route(test_client: FlaskClient, expected_years) -> None:
    response = test_client.get("/years")
    assert response.status_code == 200
    assert json.loads(response.data) == list(expected_years[0])


@pytest.mark.parametrize(
    "rcs_id, expected_name, expected_department",
    [
        ("cenzar", "Raf Cenzano", "Computer Science"),
        ("led", "Duy Le", "Computer Science"),
        ("rami", "Rami Rami", "Materials Engineering"),
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
