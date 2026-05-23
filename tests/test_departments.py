"""
Test department routes
"""

import pytest
from flask import json
from flask.testing import FlaskClient

from tests.helpers import apply_response_checks

ALL_DEPARTMENTS_CHECKS = [
    {
        "field": "name",
        "values": [
            "Computer Science",
            "Biology",
            "Materials Engineering",
            "Environmental Engineering",
            "Math",
            "Mechanical, Aerospace, and Nuclear Engineering",
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
        ],
    },
    {
        "field": "school_id",
        "values": [
            "School of Science",
            "School of Engineering",
        ],
    },
    {
        "field": "id",
        "values": ["CSCI", "BIOL", "MTLE", "ENVE", "MATH", "MANE"],
    },
    {
        "field": "image",
        "values": ["https://cdn-icons-png.flaticon.com/512/5310/5310672.png"],
    },
    {"field": "website", "values": ["https://www.rpi.edu"]},
]


@pytest.mark.parametrize(
    "endpoint, request_json, expected_status, expected_response_checks",
    [
        ("/departments", None, 200, ALL_DEPARTMENTS_CHECKS),
        (
            "/departments/CSCI",
            None,
            200,
            [
                {"field": "name", "values": ["Computer Science"]},
                {"field": "description", "values": ["DS is rough"]},
                {"field": "id", "values": ["CSCI"]},
                {
                    "field": "image",
                    "values": [
                        "https://cdn-icons-png.flaticon.com/512/5310/5310672.png"
                    ],
                },
                {"field": "website", "values": ["https://www.rpi.edu"]},
                {
                    "field": "staff",
                    "subfields": [
                        {
                            "subfield": "name",
                            "values": [
                                "Duy Le",
                                "Raf Cenzano",
                                "Wes Turner",
                                "Konstantine Kuzmin",
                                "David Goldschmidt",
                                "RCOS RCOS",
                            ],
                        },
                        {
                            "subfield": "id",
                            "values": [
                                "led",
                                "cenzar",
                                "turner",
                                "kuzmin",
                                "goldd",
                                "test",
                                "test2",
                                "test3",
                            ],
                        },
                    ],
                },
            ],
        ),
        (
            "/departments/BIOL",
            None,
            200,
            [
                {"field": "name", "values": ["Biology"]},
                {"field": "id", "values": ["BIOL"]},
            ],
        ),
        (
            "/departments/MATH",
            None,
            200,
            [
                {"field": "name", "values": ["Math"]},
                {"field": "id", "values": ["MATH"]},
            ],
        ),
        (
            "/departments/UNKNOWN",
            None,
            404,
            None,
        ),
        ("/department", None, 404, None),
        ("/department", {"wrong": "wrong"}, 404, None),
    ],
)
def test_department_routes(
    test_client: FlaskClient,
    endpoint,
    request_json,
    expected_status,
    expected_response_checks,
) -> None:
    response = (
        test_client.get(endpoint, json=request_json)
        if request_json
        else test_client.get(endpoint)
    )
    assert response.status_code == expected_status

    if expected_response_checks is None:
        return

    json_data = json.loads(response.data)
    is_list = endpoint == "/departments"
    apply_response_checks(json_data, expected_response_checks, is_list=is_list)
