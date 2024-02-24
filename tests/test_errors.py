"""
Test errors
"""

import json


def test_404_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/abcsd' page is requested (GET)
    THEN check that the response is the 404 page
    """
    response = test_client.get("/abcsd")
    assert response.status_code == 404
    print(json.loads(response.data))
    assert {"error": "404 not found"} == json.loads(response.data)


def test_500_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/professor/<professor>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/500")
    assert response.status_code == 500
    assert {"error": "500 server error. You can report issues here: https://github.com/RafaelCenzano/LabConnect/issues"}  == json.loads(response.data)
