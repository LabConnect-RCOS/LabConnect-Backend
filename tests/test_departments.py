"""
Test department routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "endpoint, request_json, expected_status, expected_response_checks",
    [
        (
            "/departments",
            None,
            200,
            [
                {
                    "field": "name",
                    "values": [
                        "Computer Science",
                        "Biology",
                        "Materials Engineering",
                        "Environmental Engineering",
                        "Math",
                        "Aerospace Engineering",
                        "Aeronautical Engineering",
                        "Mechanical, Aerospace, and Nuclear Engineering"
                    ],
                },
                {
                    "field": "description",
                    "values": [
                        "DS is rough",
                        "life science",
                        "also pretty cool",
                        "water stuff",
                        "quick maths",
                        "space, the final frontier",
                        "flying, need for speed",
                    ],
                },
                {
                    "field": "school_id",
                    "values": [
                        "School of Science",
                        "School of Science",
                        "School of Engineering",
                        "School of Science",
                        "School of Engineering",
                        "School of Engineering",
                        "School of Engineering",
                    ],
                },
                {
                    "field": "id",
                    "values": ["CSCI", "BIOL", "MTLE", "MATH", "ENVE", "MANE"],
                },
                {
                    "field": "image",
                    "values": [
                        "https://cdn-icons-png.flaticon.com/512/5310/5310672.png"
                    ]
                    * 7,
                },
                {"field": "website", "values": ["https://www.rpi.edu"] * 7},
            ],
        ),
        (
            "/department",
            {"department": "Computer Science"},
            200,
            [
                {"field": "name", "values": ["Computer Science"]},
                {"field": "description", "values": ["DS"]},
                {"field": "school_id", "values": ["School of Science"]},
                {"field": "id", "values": ["CSCI"]},
                {
                    "field": "image",
                    "values": [
                        "https://cdn-icons-png.flaticon.com/512/5310/5310672.png"
                    ],
                },
                {"field": "website", "values": ["https://www.rpi.edu"]},
                {
                    "field": "professors",
                    "subfields": [
                        {
                            "subfield": "name",
                            "values": [
                                "Duy Le",
                                "Rafael",
                                "Turner",
                                "Kuzmin",
                                "Goldschmidt",
                            ],
                        },
                        {
                            "subfield": "rcs_id",
                            "values": ["led", "cenzar", "turner", "kuzmin", "goldd"],
                        },
                    ],
                },
                {
                    "field": "opportunities",
                    "subfields": [
                        {"subfield": "id", "values": [1, 2]},
                        {
                            "subfield": "name",
                            "values": [
                                "Automated Cooling System",
                                "Iphone 15 durability test",
                            ],
                        },
                    ],
                },
            ],
        ),
        ("/department", None, 400, None),
        ("/department", {"wrong": "wrong"}, 400, None),
    ],
)
def test_department_routes(
    test_client: FlaskClient,
    endpoint,
    request_json,
    expected_status,
    expected_response_checks,
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN various '/departments' or '/department' routes are requested (GET)
    THEN check that the response status and data are as expected
    """
    response = (
        test_client.get(endpoint, json=request_json)
        if request_json
        else test_client.get(endpoint)
    )
    assert response.status_code == expected_status

    if expected_response_checks:
        json_data = json.loads(response.data)

        for check in expected_response_checks:
            if "subfields" not in check:
                for item in json_data:
                    assert item[check["field"]] in check["values"]
            else:
                for item in json_data.get(check["field"], []):
                    for subfield_check in check["subfields"]:
                        assert (
                            item[subfield_check["subfield"]] in subfield_check["values"]
                        )
