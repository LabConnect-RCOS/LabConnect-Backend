import json

import pytest
from flask.testing import FlaskClient

from tests.conftest import requires_postgres


@pytest.mark.parametrize(
    "opportunity_id, expected_data",
    [
        (
            1,
            {
                "name": "Automated Cooling System",
                "description": "Energy efficient AC system",
                "recommended_experience": "Thermodynamics",
                "pay": 15.0,
                "one_credit": False,
                "two_credits": False,
                "three_credits": False,
                "four_credits": True,
                "semester": "Spring",
                "year": 2025,
                "active": True,
            },
        ),
        (
            2,
            {
                "name": "Iphone 15 durability test",
                "description": "Scratching the Iphone, drop testing etc.",
                "recommended_experience": (
                    "Experienced in getting angry and throwing temper tantrum"
                ),
                "pay": None,
                "one_credit": True,
                "two_credits": True,
                "three_credits": True,
                "four_credits": True,
                "semester": "Spring",
                "year": 2025,
                "active": True,
            },
        ),
        (
            3,
            {
                "name": "Checking out cubes",
                "semester": "Fall",
                "year": 2025,
                "active": True,
            },
        ),
        (
            4,
            {
                "name": "Test the water",
                "semester": "Summer",
                "year": 2025,
                "active": True,
            },
        ),
    ],
)
def test_get_opportunity_parametrized(
    test_client: FlaskClient, opportunity_id, expected_data
):
    response = test_client.get("/opportunity", json={"id": opportunity_id})
    assert response.status_code == 200

    json_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert json_data[key] == value


@pytest.mark.parametrize(
    "path_id, expected_name",
    [
        (1, "Automated Cooling System"),
        (2, "Iphone 15 durability test"),
        (3, "Checking out cubes"),
        (4, "Test the water"),
    ],
)
def test_get_opportunity_by_path(
    test_client: FlaskClient, path_id: int, expected_name: str
):
    response = test_client.get(f"/opportunity/{path_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == path_id
    assert data["name"] == expected_name


@pytest.mark.parametrize(
    "request_kwargs, expected_status",
    [
        ({}, (400, 415)),
        ({"json": {"wrong": "wrong"}}, (400,)),
        ({"json": {"id": "not-an-int"}}, (400,)),
    ],
)
def test_get_opportunity_errors(
    test_client: FlaskClient, request_kwargs, expected_status
):
    response = test_client.get("/opportunity", **request_kwargs)
    if isinstance(expected_status, tuple):
        assert response.status_code in expected_status
    else:
        assert response.status_code == expected_status


@pytest.mark.parametrize(
    "missing_id",
    [999999],
)
def test_get_opportunity_not_found(test_client: FlaskClient, missing_id: int):
    response = test_client.get("/opportunity", json={"id": missing_id})
    assert response.status_code == 404


@requires_postgres
@pytest.mark.parametrize(
    "opp_id, expected_name, expected_department",
    [
        (1, "Automated Cooling System", "CSCI"),
        (2, "Iphone 15 durability test", "CSCI"),
    ],
)
def test_get_opportunity_detail(
    test_client: FlaskClient, opp_id: int, expected_name: str, expected_department: str
):
    response = test_client.get(f"/getOpportunity/{opp_id}")
    assert response.status_code == 200

    opp = json.loads(response.data)["data"]
    assert opp["name"] == expected_name
    assert opp["department"] == expected_department
    assert "authors" in opp
    assert "recommended_class_years" in opp


@pytest.mark.parametrize(
    "endpoint, expected_min_cards",
    [
        ("/staff/opportunities/led", 2),
        ("/profile/opportunities/cenzar", 2),
        ("/profile/opportunities/test", 2),
    ],
)
def test_opportunity_card_routes(
    test_client: FlaskClient, endpoint, expected_min_cards, auth_headers
):
    headers = auth_headers("test@rpi.edu")
    response = test_client.get(endpoint, headers=headers)
    assert response.status_code == 200

    cards = json.loads(response.data)
    assert len(cards) >= expected_min_cards
    for card in cards:
        assert "id" in card
        assert "title" in card
        assert "due" in card
        assert "credits" in card
