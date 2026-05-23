"""
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable

In sqlalchemy, build queries with the Executable class. (Builder design pattern)
Then pass an Executable into Session.execute()
"""

import re
import sys

import requests

from labconnect import create_app, db
from labconnect.models import (
    ClassYears,
    Codes,
    Courses,
    Leads,
    Majors,
    Opportunities,
    Participates,
    RecommendsClassYears,
    RecommendsCourses,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
    User,
    UserCourses,
    UserDepartments,
    UserMajors,
    UserSavedOpportunities,
)

url_regex = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$")


def fetch_json_data(json_url):
    response = requests.get(json_url)

    if response.status_code != 200:
        raise ValueError(f"Error: Received status code {response.status_code}")
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        raise ValueError("Error: Received invalid JSON response")


def insert_courses_from_json(session, courses_data):
    # Fetch existing courses to avoid multiple queries
    existing_courses = {course.code: course for course in session.query(Courses).all()}
    new_courses = []

    for course, course_info in courses_data.items():
        course_name = course_info.get("name")
        course_code = course_info.get("subj") + course_info.get("crse")

        if len(course_code) != 8:
            continue
        if course_code in existing_courses:
            existing_course = existing_courses[course_code]
            # Update name if changed
            if existing_course.name != course_name:
                existing_course.name = course_name
        else:
            new_course = Courses()
            new_course.code = course_code
            new_course.name = course_name
            new_courses.append(new_course)

    if new_courses:
        session.add_all(new_courses)
        session.commit()


def insert_schools_and_departments(session, schools_data):
    # Fetch existing schools and departments once
    existing_schools = {
        school.name: school for school in session.query(RPISchools).all()
    }
    existing_departments = {
        dept.id: dept for dept in session.query(RPIDepartments).all()
    }
    new_schools = []
    new_depts = []

    for school_data in schools_data:
        school_name = school_data.get("name")
        school_description = ""

        if school_name in existing_schools:
            school = existing_schools[school_name]
            # Update description if changed
            if school.description != school_description:
                school.description = school_description
        else:
            new_school = RPISchools()
            new_school.name = school_name
            new_school.description = school_description
            new_schools.append(new_school)

        for department_data in school_data.get("depts", []):
            department_id = department_data.get("code")
            department_name = department_data.get("name")
            department_description = ""

            if department_id in existing_departments:
                department = existing_departments[department_id]
                # Update name or description if changed
                if department.name != department_name:
                    department.name = department_name
                if department.description != department_description:
                    department.description = department_description
                if department.school_id != school_name:
                    department.school_id = school_name
            else:
                new_department = RPIDepartments()
                new_department.id = department_id
                new_department.name = department_name
                new_department.description = department_description
                new_department.school_id = school_name
                new_depts.append(new_department)

    if new_schools or new_depts:
        session.add_all(new_schools + new_depts)
        session.commit()


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("No argument or existing argument found")

    if sys.argv[1] == "start":
        app = create_app()
        with app.app_context():
            if not db.inspect(db.engine).get_table_names():
                db.create_all()

    elif sys.argv[1] == "clear":
        app = create_app()
        with app.app_context():
            db.drop_all()

    elif sys.argv[1] == "addCourses":
        if len(sys.argv) < 3:
            sys.exit("Error: No URL argument provided.")

        j_url = sys.argv[2]

        # Validate that j_url is a valid URL
        if not url_regex.match(j_url):
            sys.exit("Error: Invalid URL provided.")

        app = create_app()
        with app.app_context():
            db.create_all()

            data = fetch_json_data(j_url)
            if not data:
                sys.exit("Failed to fetch courses data. Exiting...")

            insert_courses_from_json(db.session, data)

            db.session.close()

    elif sys.argv[1] == "addDept":
        if len(sys.argv) < 3:
            sys.exit("Error: No URL argument provided.")

        j_url = sys.argv[2]

        # Validate that j_url is a valid URL
        if not url_regex.match(j_url):
            sys.exit("Error: Invalid URL provided.")

        app = create_app()
        with app.app_context():
            db.create_all()

            data = fetch_json_data(j_url)
            if not data:
                sys.exit("Failed to fetch schools data. Exiting...")

            insert_schools_and_departments(db.session, data)

            db.session.close()

    elif sys.argv[1] == "create":
        app = create_app()
        with app.app_context():
            db.create_all()

            from tests.seed import seed_development_data

            seed_development_data()

            tables = [
                ClassYears,
                Courses,
                Leads,
                Majors,
                Opportunities,
                Participates,
                RecommendsClassYears,
                RecommendsCourses,
                RecommendsMajors,
                RPIDepartments,
                RPISchools,
                User,
                UserCourses,
                UserDepartments,
                UserMajors,
                UserSavedOpportunities,
                Codes,
            ]

            for table in tables:
                stmt = db.select(table)
                result = db.session.execute(stmt).scalars()

                inst = db.inspect(table)
                attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]

                app.logger.info(f"{table.__tablename__}")
                app.logger.info(attr_names)
                for row in result:
                    app.logger.info(row)

            print("Number of tables:", len(tables))


if __name__ == "__main__":
    main()
