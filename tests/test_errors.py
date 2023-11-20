"""
Test errors
"""


def test_404_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/abcsd' page is requested (GET)
    THEN check that the response is the 404 page
    """
    response = test_client.get("/abcsd")
    assert response.status_code == 404
    assert b"404 Not Found" in response.data
    assert b"This page was not found" in response.data
    assert b"Return Home" in response.data
    assert b"If you believe this is a bug or error please create an" in response.data
    assert (
        b'href="https://github.com/RafaelCenzano/LabConnect/issues">Issue'
        in response.data
    )


def test_500_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/professor/<professor>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/professor/duncan")
    assert response.status_code == 500
    assert b"500 Server Error" in response.data
    assert b"The server had an error" in response.data
    assert b"Return Home" in response.data
    assert b"If you believe this is a bug or error please create an" in response.data
    assert (
        b'href="https://github.com/RafaelCenzano/LabConnect/issues">Issue'
        in response.data
    )
