import pytest


def test_opportunity_to_dict_none():
    from importlib import import_module
    opp_mod = import_module("labconnect.main.opportunity_routes")
    assert opp_mod.opportunity_to_dict(None) == {}


def test_opportunity_to_dict_populated():
    # create a lightweight Opportunities instance (no DB persistence needed)
    from labconnect.models import Opportunities
    
    opp = Opportunities()
    opp.id = 123
    opp.name = "Unit Test Opportunity"
    opp.description = "A test description"
    opp.recommended_experience = "Testing"
    opp.pay = 7.5
    opp.one_credit = True
    opp.two_credits = False
    opp.three_credits = False
    opp.four_credits = False
    opp.semester = None
    opp.year = 2025
    opp.active = True

    from importlib import import_module
    opp_mod = import_module("labconnect.main.opportunity_routes")
    out = opp_mod.opportunity_to_dict(opp)

    assert out["id"] == 123
    assert out["name"] == "Unit Test Opportunity"
    assert out["pay"] == 7.5
    assert out["one_credit"] is True
    assert out["two_credits"] is False
    assert out["semester"] is None
    assert out["year"] == 2025


@pytest.mark.usefixtures("test_client")
def test_get_single_opportunity_not_found(test_client):
    response = test_client.get("/opportunity/999999")
    assert response.status_code == 404


@pytest.mark.usefixtures("test_client")
def test_get_single_opportunity_success_and_json_variant(test_client):
    # create and persist an opportunity to the test database
    from labconnect import db
    from labconnect.models import Opportunities
    
    opp = Opportunities()
    opp.name = "Endpoint Test Opportunity"
    opp.description = "Endpoint description"
    opp.recommended_experience = "None"
    opp.pay = 12.0
    opp.one_credit = False
    opp.two_credits = True
    opp.three_credits = False
    opp.four_credits = False
    opp.semester = None
    opp.year = 2025
    opp.application_due = None
    opp.active = True
    opp.last_updated = None
    opp.location = None

    db.session.add(opp)
    db.session.commit()

    # GET by URL id
    resp = test_client.get(f"/opportunity/{opp.id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == opp.id
    assert data["name"] == "Endpoint Test Opportunity"
    assert data["pay"] == 12.0

    # GET via JSON body variant
    resp2 = test_client.get("/opportunity", json={"id": opp.id})
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert data2["id"] == opp.id


@pytest.mark.usefixtures("test_client")
def test_get_opportunity_via_json_errors(test_client):
    # No JSON -> 400
    resp = test_client.get("/opportunity")
    assert resp.status_code in (400, 415)

    # Missing id key -> 400
    resp2 = test_client.get("/opportunity", json={"wrong": "key"})
    assert resp2.status_code == 400

    # Non-integer id -> 400
    resp3 = test_client.get("/opportunity", json={"id": "not-an-int"})
    assert resp3.status_code == 400
