import json
import pytest
from flask.testing import FlaskClient

def test_get_opportunity_parametrized(test_client: FlaskClient):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET) with different IDs
    THEN check that the responses are valid
    """
    test_cases = [
        (1, {
            "name": "Automated Cooling System",
            "description": "Energy efficient AC system",
            "recommended_experience": "Thermodynamics",
            "pay": 15.0,
            "one_credit": False,
            "two_credits": False,
            "three_credits": False,
            "four_credits": True,
            "semester": "Spring",
            "year": 2024,
            "active": True,
        }),
        (2, {
            "name": "Iphone 15 durability test",
            "description": "Scratching the Iphone, drop testing etc.",
            "recommended_experience": "Experienced in getting angry and throwing temper tantrum",
            "pay": None,
            "one_credit": True,
            "two_credits": True,
            "three_credits": True,
            "four_credits": True,
            "semester": "Spring",
            "year": 2024,
            "active": True,
        }),
    ]

    for opportunity_id, expected_data in test_cases:
        response = test_client.get("/opportunity", json={"id": opportunity_id})
        assert response.status_code == 200

        json_data = json.loads(response.data)
        for key, value in expected_data.items():
            assert json_data[key] == value


def test_get_opportunity_no_json(test_client: FlaskClient):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET) without JSON payload
    THEN check that the response is 400
    """
    response = test_client.get("/opportunity")
    assert response.status_code == 400


def test_opportunity_incorrect_json(test_client: FlaskClient):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity' page is requested (GET) with incorrect JSON
    THEN check that the response is 400
    """
    response = test_client.get("/opportunity", json={"wrong": "wrong"})
    assert response.status_code == 400


@pytest.mark.parametrize(
    "endpoint, expected_keys",
    [
        ("/getOpportunityMeta/1", [
            "name",
            "description",
            "recommended_experience",
            "pay",
            "credits",
            "semester",
            "year",
            "application_due",
            "active",
            "courses",
            "majors",
            "years",
        ]),
        ("/getOpportunity/2", [
            "id",
            "name",
            "description",
            "recommended_experience",
            "author",
            "department",
            "aboutSection",
        ]),
    ],
)
def test_opportunity_meta_parametrized(test_client: FlaskClient, endpoint, expected_keys):
    """
    GIVEN a Flask application configured for testing
    WHEN specific opportunity endpoints are requested
    THEN check that the response contains the expected keys
    """
    response = test_client.get(endpoint, content_type="application/json")
    assert response.status_code == 200

    data = json.loads(response.data)
    if "data" in data:
        data = data["data"]

    for key in expected_keys:
        if isinstance(data, list):
            for item in data:
                assert key in item
        else:
            assert key in data


@pytest.mark.parametrize(
    "endpoint", [
        "/getOpportunityByProfessor/led",
        "/getProfessorOpportunityCards/led",
        "/getProfileOpportunities/led",
    ]
)
def test_professor_related_opportunities(test_client: FlaskClient, endpoint):
    """
    GIVEN a Flask application configured for testing
    WHEN professor-related endpoints are requested
    THEN check that the response contains expected keys in each card
    """
    response = test_client.get(endpoint, content_type="application/json")
    assert response.status_code == 200

    data = json.loads(response.data)["data"]
    for each_card in data:
        assert "id" in each_card
        assert "title" in each_card or "name" in each_card
        assert "body" in each_card or "description" in each_card
        assert "attributes" in each_card or "recommended_experience" in each_card
