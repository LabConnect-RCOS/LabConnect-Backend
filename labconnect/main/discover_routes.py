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
    result = discover_data(get_jwt_identity(), 5)
    return result

def discover_data(jwt_identity, limit):
    data = []
    if jwt_identity is not None:
        user = db.select(User).where(User.email == jwt_identity).first()
        query = (
            db.select(
                Opportunities,
            )
            .where(
                Opportunities.active == True
            )
            .join(RecommendsClassYears, Opportunities.id == RecommendsClassYears.class_year)
            .join(ClassYears, RecommendsClassYears.class_year == ClassYears.class_year)
            .where(
                ClassYears.class_year == user.class_year
            )
            .limit(limit)
            .order_by(Opportunities.last_updated.desc())
        )

        majors = [Majors.code == user_major.major_code for user_major in db.select(UserMajors).where(UserMajors.user_id == user.id).scalars()]
        query = query.join(Majors, RecommendsMajors.major_code == Majors.code)
        query = query.where(db.or_(*majors))

        data = db.session.execute(query).scalars()
    if jwt_identity is None or data is None:
        data = db.session.execute(db.select(Opportunities).where(Opportunities.active == True).limit(limit).order_by(Opportunities.last_updated.desc()))
    result = [opportunity.to_dict() for opportunity in data]
    return result