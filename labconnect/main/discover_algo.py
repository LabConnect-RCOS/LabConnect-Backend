#This page is for the Discover page's algorithm

from labconnect import db
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
from sqlalchemy import text


def return_query():
    # return the query
    query = (
        # db.select(
        #     Opportunities.name
        # )
        db.select(
            Opportunities,
            Majors,
            RecommendsMajors,
            RecommendsClassYears,
            ClassYears,
        )
        .filter(Majors.code == "CSCI") # in future: major_code: intake someone's department/major
        .filter(ClassYears.class_year == "2024") # match school year of student to oppoortunity

        .filter(Opportunities.active == True) # ensure opportunity is active & not past the deadline
        .join(RecommendsMajors, Opportunities.id == RecommendsMajors.opportunity_id)
        .join(Majors, RecommendsMajors.major_code == Majors.code)
        #.join(Opportunities, RecommendsMajors.opportunity_id == Opportunities.id)
        

        .join(RecommendsClassYears, Opportunities.id == RecommendsClassYears.class_year)
        .join(ClassYears, RecommendsClassYears.class_year == ClassYears.class_year)
        #joining cannot take itself
        #.join(Opportunities, RecommendsClassYears.opportunity_id == Opportunities.id)

        .limit(4) # limit how many things are returned from the query (4 items)
    )

    print(query)
    data = db.session.execute(query)
    #data = db.session.execute(text('SELECT 1')
    print("HERE")
    print(data)
    return data





