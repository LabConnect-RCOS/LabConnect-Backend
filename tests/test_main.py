import json

"""
Test mains
"""

from flask import json
from flask.testing import FlaskClient

from labconnect import db
from labconnect.helpers import OrJSONProvider, SemesterEnum
from labconnect.models import (
    ClassYears,
    Courses,
    LabManager,
    Leads,
    Majors,
    Opportunities,
    RecommendsClassYears,
    RecommendsCourses,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
)


def test_professor_profile(test_client: FlaskClient) -> None:

    response = test_client.get("/getProfessorProfile/cenzar")
    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data)

    # Test that the "name" key exists
    assert "name" in data
    assert "image" in data
    assert "department" in data
    assert "description" in data
    assert "role" in data
    assert "phone_number" in data
    assert "email" in data
    assert "alt_email" in data
    assert "website" in data
    assert "phone" in data
    assert "role" in data


def test_get_opportunity(test_client: FlaskClient) -> None:
    response = test_client.get("/getOpportunity/2")

    assert response.status_code == 200

    # Load the response data as JSON
    data = json.loads(response.data.decode("utf-8"))
    data = data["data"]

    # Test that the "name" key exists
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "recommended_experience" in data
    assert "author" in data
    assert "department" in data
    assert "aboutSection" in data

    for eachSection in data["aboutSection"]:
        assert "title" in eachSection
        assert "description" in eachSection


# def test_schools_and_departments(test_client: FlaskClient) -> None:
#     response = test_client.get(
#         "/getSchoolsAndDepartments", content_type="application/json"
#     )

#     assert response.status_code == 200

#     data = json.loads(response.data.decode("utf-8"))

#     assert "School of Science" in data
#     assert "School of Engineering" in data

#     query = db.session.execute(
#         db.select(RPISchools, RPIDepartments).join(
#             RPIDepartments, RPISchools.name == RPIDepartments.school_id
#         )
#     )

#     results = query.all()

#     # check that all the schools and department are in the data and are accurate
#     for tuple in results:
#         assert tuple[1].name in data[tuple[0].name]
