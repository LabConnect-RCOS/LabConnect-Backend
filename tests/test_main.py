"""
Test mains
"""


def test_home_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"LabConnect" in response.data
    assert b"Your Recommendations" in response.data


def test_opportunities_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunities' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/opportunities")
    assert response.status_code == 200
    assert b"Applied" in response.data
    assert b"Saved" in response.data
    assert b"Filters" in response.data


def test_opportunity_detail_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/opportunity/<int:id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/opportunity/4")
    assert response.status_code == 200
    assert b"Quantum Computing to solve NP-Complete Problems" in response.data
    assert b"About This Role" in response.data
    assert b"Deadline" in response.data


def test_discover_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/discover' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/discover")
    assert response.status_code == 200
    assert b"Departments" in response.data
    assert b"Research Centers" in response.data


def test_create_post_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/create_post' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/create_post")
    assert response.status_code == 200
    assert b"Title" in response.data
    assert b"Major" in response.data
    assert b"Term" in response.data
    assert b"Deadline" in response.data
    assert b"Grade" in response.data
    assert b"Description" in response.data
    assert b"Compensation" in response.data
    assert b"Submit" in response.data


def test_login_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Please sign in" in response.data


def test_department_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/department/<department>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/department/bob")
    assert response.status_code == 200
    assert b"Research Centers" in response.data
    assert b"Professors" in response.data


def test_professor_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/professor/<professor>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/professor/bob")
    assert response.status_code == 200
    assert b"Name:" in response.data
    assert b"Department:" in response.data
    assert b"Contact:" in response.data


def test_profile_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/profile/bob")
    assert response.status_code == 200
    assert b"Name:" in response.data
    assert b"Department:" in response.data
    assert b"Contact:" in response.data


def test_tips_and_tricks_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/tips")
    assert response.status_code == 200
    assert b"Tips and Tricks for LabConnect" in response.data


def test_info_page(test_client) -> None:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile/<user>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/info")
    assert response.status_code == 200
    assert b"URP for Credit" in response.data
    assert b"URP for Funding" in response.data

    response = test_client.get("/information")
    assert response.status_code == 200
    assert b"URP for Credit" in response.data
    assert b"URP for Funding" in response.data
