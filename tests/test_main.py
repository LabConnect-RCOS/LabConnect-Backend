"""
Test mains
"""


def test_home_page_with_fixture(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"LabConnect" in response.data