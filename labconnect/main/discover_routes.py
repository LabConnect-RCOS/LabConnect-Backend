import datetime
from typing import Any

from flask import abort, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)

from labconnect import bcrypt, db
from .discover_routes import *
from labconnect.helpers import SemesterEnum
from labconnect.models import (
    ClassYears,
    Courses,
    LabManager,
    Leads,
    Majors,
    Opportunities,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
    User,
    UserCourses,
    UserDepartments,
    UserMajors,
    Participates,
    RecommendsCourses,
    RecommendsClassYears,
)

from . import main_blueprint


@main_blueprint.get("/discover")
def discover():
    query = (
        db.select(
            Opportunities,
        )
        .where(
            Majors.code == "CSCI"
        )  # in future: major_code: intake someone's department/major
        # .where(
        #     ClassYears.class_year == "2024"
        # )  # match school year of student to oppoortunity
        .where(
            Opportunities.active == True
        )  # ensure opportunity is active & not past the deadline
        .join(RecommendsMajors, Opportunities.id == RecommendsMajors.opportunity_id)
        .join(Majors, RecommendsMajors.major_code == Majors.code)
        # .join(Opportunities, RecommendsMajors.opportunity_id == Opportunities.id)
        .join(RecommendsClassYears, Opportunities.id == RecommendsClassYears.class_year)
        .join(ClassYears, RecommendsClassYears.class_year == ClassYears.class_year)
        .limit(5)  # limit how many things are returned from the query (4 items)
        .order_by(Opportunities.last_updated.desc())
    )

    print(query)
    data = db.session.execute(query)
    print("HERE")
    print(data)
    result = [opportunity.to_dict() for opportunity in data]
    return result


# example json below
#     "data": [
#         {
#             "title": "Nelson",
#             "major": "CS",
#             # "experience": "x",
#             # "description": "d",
#             "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
#             "credits": 4,
#             "pay": 9000.0,
#         },
#         {
#             "title": "Name",
#             "major": "Major",
#             # "experience": "XP",
#             # "description": "Hi",
#             "attributes": ["Competitive Pay", "Four Credits", "Three Credits"],
#             "credits": 3,
#             "pay": 123,
#         },
#     ]
