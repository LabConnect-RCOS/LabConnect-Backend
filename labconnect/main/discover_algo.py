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

def return_query():
    # return the query
    query = (
        db.select(
            Opportunities.id,
            Opportunities.name,
            Opportunities.description,
            Opportunities.pay,
            Opportunities.credits,
            Majors,
            RecommendsMajors,
            RecommendsClassYears,
            ClassYears,
        )
        .filter(Majors.code == "CSCI") # in future: major_code: intake someone's department/major

        .filter(ClassYears.class_year == "2024")

        .join(Opportunities, Opportunities.id == RecommendsMajors.opportunity_id)
        .join(Majors, RecommendsMajors.major_code == Majors.code)
        .join(Opportunities, Opportunities.id == RecommendsClassYears.opportunity_id)

        .join(ClassYears, ClassYears.class_year == RecommendsClassYears.class_year)
    )

    print(query)
    data = db.session.execute(query)
    print(data)
    return query


# limit how many things are returned from the query (4 items)
# match school year of student to oppoortunity
# ensure opportunity is active & not past the deadline

