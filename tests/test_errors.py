"""
Test errors
"""


def test_404_page_with_fixture(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/abcsd' page is requested (GET)
    THEN check that the response is the 404 page
    """
    response = test_client.get("/abcsd")
    assert response.status_code == 404
    assert b"Not Found" in response.data
    assert (
        b"The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
        in response.data
    )
