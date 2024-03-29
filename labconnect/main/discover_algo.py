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
        db.select(
            Opportunities.name
        )
        # db.select(
        #     Opportunities.id,
        #     Opportunities.name,
        #     Opportunities.description,
        #     Opportunities.pay,
        #     Opportunities.credits,
        #     Opportunities.active,
        #     Majors,
        #     RecommendsMajors,
        #     RecommendsClassYears,
        #     ClassYears,
        # )
        # .filter(Majors.code == "CSCI") # in future: major_code: intake someone's department/major
        # .filter(ClassYears.class_year == "2024") # match school year of student to oppoortunity

        # .filter(Opportunities.active == True) # ensure opportunity is active & not past the deadline
        # .join(RecommendsMajors, Majors.code == RecommendsMajors.major_code)
        # .join(Opportunities, Opportunities.id == RecommendsMajors.opportunity_id)
        
        # .join(RecommendsClassYears, ClassYears.class_year == RecommendsClassYears.class_year)
        
        # .join(Opportunities, Opportunities.id == RecommendsClassYears.opportunity_id)
        

        # .limit(4) # limit how many things are returned from the query (4 items)
    )

    print(query)
    data = db.session.execute(query)
    #data = db.session.execute(text('SELECT 1')
    print("HERE")
    print(data)
    return data





