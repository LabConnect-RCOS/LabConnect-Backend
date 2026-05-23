"""
Test majors routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "expected_codes, expected_names",
    [
        (
            ("BIOL", "COGS", "CSCI", "ECSE", "MATH", "PHYS"),
            (
                "Biological Science",
                "Cognitive Science",
                "Computer Science",
                "Electrical, Computer, and Systems Engineering",
                "Mathematics",
                "Physics",
            ),
        ),
    ],
)
def test_majors_route(test_client: FlaskClient, expected_codes, expected_names) -> None:
    response = test_client.get("/majors")
    assert response.status_code == 200

    json_data = json.loads(response.data)
    assert len(json_data) == len(expected_codes)

    codes = {major["code"] for major in json_data}
    names = {major["name"] for major in json_data}
    assert codes == set(expected_codes)
    assert names == set(expected_names)


@pytest.mark.parametrize(
    "major_code, major_name",
    [
        ("CSCI", "Computer Science"),
        ("ECSE", "Electrical, Computer, and Systems Engineering"),
        ("BIOL", "Biological Science"),
        ("MATH", "Mathematics"),
        ("COGS", "Cognitive Science"),
        ("PHYS", "Physics"),
    ],
)
def test_majors_route_each_major(
    test_client: FlaskClient, major_code: str, major_name: str
) -> None:
    response = test_client.get("/majors")
    assert response.status_code == 200

    match = next(
        (major for major in json.loads(response.data) if major["code"] == major_code),
        None,
    )
    assert match is not None
    assert match["name"] == major_name


@pytest.mark.parametrize(
    "invalid_method, expected_status",
    [
        ("post", 405),
    ],
)
def test_majors_route_invalid_method(
    test_client: FlaskClient, invalid_method: str, expected_status: int
) -> None:
    response = getattr(test_client, invalid_method)("/majors")
    assert response.status_code == expected_status
