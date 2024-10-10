import pytest
import json
from flask.testing import FlaskClient
from labconnect import db
from labconnect.models import Opportunities


@pytest.mark.parametrize(
    "opportunity_id, expected_data",
    [
        (
            1,
            (
                "Automated Cooling System",
                "Energy efficient AC system",
                "Thermodynamics",
                15.0,
                False,
                False,
                False,
                True,
                "Spring",
                2024,
                True,
            ),
        ),
        (
            2,
            (
                "Iphone 15 durability test",
                "Scratching the Iphone, drop testing etc.",
                "Experienced in getting angry and throwing temper tantrum",
                None,
                True,
                True,
                True,
                True,
                "Spring",
                2024,
                True,
            ),
        ),
    ],
)
def test_get_opportunity(test_client: FlaskClient, opportunity_id, expected_data) -> None:
    response = test_client.get("/opportunity", json={"id": opportunity_id})

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert json_data["name"] == expected_data[0]
    assert json_data["description"] == expected_data[1]
    assert json_data["recommended_experience"] == expected_data[2]
    assert json_data["pay"] == expected_data[3]
    assert json_data["one_credit"] == expected_data[4]
    assert json_data["two_credits"] == expected_data[5]
    assert json_data["three_credits"] == expected_data[6]
    assert json_data["four_credits"] == expected_data[7]
    assert json_data["semester"] == expected_data[8]
    assert json_data["year"] == expected_data[9]
    assert json_data["active"] == expected_data[10]


def test_get_opportunity_no_json(test_client: FlaskClient) -> None:
    response = test_client.get("/opportunity")
    assert response.status_code == 400


@pytest.mark.parametrize(
    "wrong_data", [{"wrong": "wrong"}, {"invalid": "data"}]
)
def test_opportunity_incorrect_json(test_client: FlaskClient, wrong_data) -> None:
    response = test_client.get("/opportunity", json=wrong_data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "opportunity_meta_id",
    [1, 2],
)
def test_get_opportunity_meta(test_client: FlaskClient, opportunity_meta_id) -> None:
    response = test_client.get(f"/getOpportunityMeta/{opportunity_meta_id}", content_type="application/json")
    data = json.loads(response.data)["data"]

    assert "name" in data
    assert "description" in data
    assert "recommended_experience" in data
    assert "pay" in data
    assert "credits" in data
    assert "semester" in data
    assert "year" in data
    assert "application_due" in data
    assert "active" in data
    assert "courses" in data
    assert "majors" in data
    assert "years" in data


@pytest.mark.parametrize(
    "opportunity_id",
    [1, 2],
)
def test_get_opportunity_by_id(test_client: FlaskClient, opportunity_id) -> None:
    response = test_client.get(f"/getOpportunity/{opportunity_id}")

    assert response.status_code == 200

    data = json.loads(response.data)["data"]

    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "recommended_experience" in data
    assert "author" in data
    assert "department" in data
    assert "aboutSection" in data

    for eachSection in data["aboutSection"]:
        assert "title" in eachSection
        assert "description" in eachSection


@pytest.mark.parametrize(
    "professor_name", ["led", "drsmith"]
)
def test_get_opportunity_professor(test_client: FlaskClient, professor_name) -> None:
    response = test_client.get(f"/getOpportunityByProfessor/{professor_name}")
    assert response.status_code == 200

    data = json.loads(response.data)["data"]

    for opportunity in data:
        assert "id" in opportunity
        assert "name" in opportunity
        assert "description" in opportunity
        assert "recommended_experience" in opportunity
        assert "pay" in opportunity
        assert "semester" in opportunity
        assert "year" in opportunity
        assert "application_due" in opportunity
        assert "active" in opportunity


@pytest.mark.parametrize(
    "professor_name", ["led", "drsmith"]
)
def test_get_professor_opportunity_cards(test_client: FlaskClient, professor_name) -> None:
    response = test_client.get(f"/getProfessorOpportunityCards/{professor_name}", content_type="application/json")
    assert response.status_code == 200

    data = json.loads(response.data)["data"]

    for eachCard in data:
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "id" in eachCard


@pytest.mark.parametrize(
    "professor_name", ["led", "drsmith"]
)
def test_profile_opportunities(test_client: FlaskClient, professor_name) -> None:
    response = test_client.get(f"/getProfileOpportunities/{professor_name}", content_type="application/json")
    assert response.status_code == 200

    data = json.loads(response.data)["data"]

    for eachCard in data:
        assert "id" in eachCard
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "activeStatus" in eachCard


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "authorID": "led",
            "name": "Some test opportunity",
            "description": "Some test description",
            "recommended_experience": "Some test experience",
            "pay": 25.0,
            "credits": ["1", "2", "3", "4"],
            "semester": "FALL",
            "year": 2024,
            "application_due": "2024-03-30",
            "active": True,
            "courses": ["CSCI4430"],
            "majors": ["BIOL"],
            "years": [2023, 2024],
            "location": "TBD",
        }
    ],
)
def test_create_opportunity(test_client: FlaskClient, test_data) -> None:
    response = test_client.post(
        "/createOpportunity",
        data=json.dumps(test_data),
        content_type="application/json",
    )
    assert response.status_code == 200

    query = db.session.query(Opportunities).filter(
        Opportunities.name == test_data["name"],
        Opportunities.description == test_data["description"],
        Opportunities.recommended_experience == test_data["recommended_experience"],
    )

    data = query.first()
    assert data is not None
    id = data.id

    response = test_client.post(
        "/deleteOpportunity",
        data=json.dumps({"id": id}),
        content_type="application/json",
    )

    assert response.status_code == 200

    query = db.session.query(Opportunities).filter(Opportunities.id == id)
    assert query.first() is None


@pytest.mark.parametrize(
    "professor_name", ["led", "drsmith"]
)
def test_professor_opportunity_cards(test_client: FlaskClient, professor_name) -> None:
    response = test_client.get(f"/getProfessorOpportunityCards/{professor_name}")
    assert response.status_code == 200

    data = json.loads(response.data)["data"]

    assert len(data.keys()) > 0
    for eachCard in data["data"]:
        assert "title" in eachCard
        assert "body" in eachCard
        assert "attributes" in eachCard
        assert "id" in eachCard
