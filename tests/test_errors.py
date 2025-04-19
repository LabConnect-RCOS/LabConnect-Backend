"""
Test errors
"""

import pytest
from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "route, expected_status, expected_response",
    [
        ("/abcsd", 404, {"error": "404 not found"}),
        (
            "/500",
            500,
            {
                "error": "500 server error. You can report issues here: https://github.com/RafaelCenzano/LabConnect/issues"
            },
        ),
    ],
)
def test_error_pages(
    test_client: FlaskClient, route, expected_status, expected_response
) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the specified error route is requested (GET)
    THEN check that the response status and data are as expected
    """
    response = test_client.get(route)
    assert response.status_code == expected_status
    assert json.loads(response.data) == expected_response
