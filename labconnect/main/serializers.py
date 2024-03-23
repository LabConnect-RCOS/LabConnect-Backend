from flask import abort, render_template, request

from labconnect import db
from labconnect.helpers import SemesterEnum
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

from . import main_blueprint

def serialize_opportunity(opportunity):
    return {
        "id": opportunity.id,
        "name": opportunity.name,
        "description": opportunity.description,
        "semester": opportunity.semester.name,
        "year": opportunity.year,
        "pay": opportunity.pay,
        "credits": opportunity.credits,
        "application_due": opportunity.application_due,
        # "lab_manager": opportunity.lab_managers.,
        # "leads": [lead.rcs_id for lead in opportunity.leads],
        # "courses": [course.course_code for course in opportunity.courses],
        # "majors": [major.major_code for major in opportunity.majors],
        # "class_years": [class_year.year for class_year in opportunity.class_years],
        # "departments": [department.department_code for department in opportunity.departments],
        # "schools": [school.school_code for school in opportunity.schools],
        
    }