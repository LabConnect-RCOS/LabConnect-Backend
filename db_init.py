"""
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable

In sqlalchemy, build queries with the Executable class. (Builder design pattern)
Then pass an Executable into Session.execute()
"""

import re
import sys
from datetime import date, datetime

import requests

from labconnect import create_app, db
from labconnect.helpers import LocationEnum, SemesterEnum
from labconnect.models import (
    ClassYears,
    Courses,
    LabManager,  # Professors and Grad students
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
    LabManager,
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

            rpi_schools_rows = (
                ("School of Science", "the coolest of them all"),
                ("School of Engineering", "also pretty cool"),
            )

            for row_tuple in rpi_schools_rows:
                row = RPISchools()
                row.name = row_tuple[0]
                row.description = row_tuple[1]

                db.session.add(row)
                db.session.commit()

            rpi_departments_rows = (
                ("Computer Science", "DS is rough", "School of Science", "CSCI"),
                ("Biology", "life science", "School of Science", "BIOL"),
                (
                    "Materials Engineering",
                    "also pretty cool",
                    "School of Engineering",
                    "MTLE",
                ),
                (
                    "Environmental Engineering",
                    "water stuff",
                    "School of Engineering",
                    "ENVE",
                ),
                ("Math", "quick maths", "School of Science", "MATH"),
                (
                    "Mechanical, Aerospace, and Nuclear Engineering",
                    "space, the final frontier",
                    "School of Engineering",
                    "MANE",
                ),
            )

            for row_tuple in rpi_departments_rows:
                row = RPIDepartments()
                row.name = row_tuple[0]
                row.description = row_tuple[1]
                row.school_id = row_tuple[2]
                row.id = row_tuple[3]
                row.image = "https://cdn-icons-png.flaticon.com/512/5310/5310672.png"
                row.website = "https://www.rpi.edu"

                db.session.add(row)
                db.session.commit()

            class_years_rows = (2025, 2026, 2027, 2028, 2029, 2030, 2031)

            for row_item in class_years_rows:
                row = ClassYears()
                row.class_year = row_item
                row.active = True

                db.session.add(row)
                db.session.commit()

            lab_manager_rows = (
                ("led", "Duy", "Le", "CSCI", "database database database"),
                (
                    "turner",
                    "Wes",
                    "Turner",
                    "CSCI",
                    "open source stuff is cool",
                ),
                (
                    "kuzmin",
                    "Konstantine",
                    "Kuzmin",
                    "CSCI",
                    "java, psoft, etc.",
                ),
                ("goldd", "David", "Goldschmidt", "CSCI", "VIM master"),
                ("rami", "Rami", "Rami", "MTLE", "cubes are cool"),
                ("holm", "Mark", "Holmes", "MATH", "all about that math"),
                ("test", "RCOS", "RCOS", "CSCI", "first test"),
                ("test2", "RCOS", "RCOS", "CSCI", "Second test"),
                ("test3", "RCOS", "RCOS", "CSCI", "Third test"),
            )

            raf_test_user = (
                "cenzar",
                "Rafael",
                "Cenzano",
                "Raf",
                2025,
                "CSCI",
                "labconnect is the best RCOS project",
                "https://rafael.sirv.com/Images/rafael.jpeg?thumbnail=350&format=webp&q=90",
                "https://rafaelcenzano.com",
            )

            lab_manager = LabManager()
            lab_manager.department_id = raf_test_user[5]

            db.session.add(lab_manager)
            db.session.commit()

            user = User()
            user.id = raf_test_user[0]
            user.email = raf_test_user[0] + "@rpi.edu"
            user.first_name = raf_test_user[1]
            user.last_name = raf_test_user[2]
            user.preferred_name = raf_test_user[3]
            user.class_year = raf_test_user[4]
            user.lab_manager_id = lab_manager.id
            user.description = raf_test_user[6]
            user.profile_picture = raf_test_user[7]
            user.website = raf_test_user[8]

            db.session.add(user)
            db.session.commit()

            for row_tuple in lab_manager_rows:
                lab_manager = LabManager()
                lab_manager.department_id = row_tuple[3]

                db.session.add(lab_manager)
                db.session.commit()

                user = User()
                user.id = row_tuple[0]
                user.email = row_tuple[0] + "@rpi.edu"
                user.first_name = row_tuple[1]
                user.last_name = row_tuple[2]
                user.lab_manager_id = lab_manager.id
                user.description = row_tuple[4]
                user.profile_picture = (
                    "https://www.svgrepo.com/show/206842/professor.svg"
                )

                db.session.add(user)
                db.session.commit()

            opportunities_rows = (
                (
                    "Automated Cooling System",
                    "Energy efficient AC system",
                    "Thermodynamics",
                    15.0,
                    False,
                    False,
                    False,
                    True,
                    SemesterEnum.SPRING,
                    2025,
                    date.today(),
                    True,
                    datetime.now(),
                    LocationEnum.REMOTE,
                ),
                (
                    "Iphone 15 durability test",
                    "Scratching the Iphone, drop testing etc.",
                    "Experienced in getting angry and throwing temper tantrum",
                    None,
                    True,
                    True,
                    True,
                    True,
                    SemesterEnum.SPRING,
                    2025,
                    date.today(),
                    True,
                    datetime.now(),
                    LocationEnum.LALLY,
                ),
                (
                    "Checking out cubes",
                    "Material Sciences",
                    "Experienced in materials.",
                    None,
                    True,
                    True,
                    True,
                    True,
                    SemesterEnum.FALL,
                    2025,
                    date.today(),
                    True,
                    datetime.now(),
                    LocationEnum.MRC,
                ),
                (
                    "Test the water",
                    "Testing the quality of water in Troy pipes",
                    "Understanding of lead poisioning",
                    None,
                    False,
                    False,
                    True,
                    True,
                    SemesterEnum.SUMMER,
                    2025,
                    date.today(),
                    True,
                    datetime.now(),
                    LocationEnum.JEC,
                ),
                (
                    "Data Science Research",
                    "Work with a team of researchers to analyze large datasets and "
                    "extract meaningful insights.",
                    "Python, Machine Learning, Data Analysis",
                    20.0,
                    True,
                    False,
                    True,
                    False,
                    SemesterEnum.FALL,
                    2025,
                    "2025-10-31",
                    True,
                    "2025-10-10T10:30:00",
                    LocationEnum.JROWL,
                ),
            )

            for row_tuple in opportunities_rows:
                row = Opportunities()
                row.name = row_tuple[0]
                row.description = row_tuple[1]
                row.recommended_experience = row_tuple[2]
                row.pay = row_tuple[3]
                row.one_credit = row_tuple[4]
                row.two_credits = row_tuple[5]
                row.three_credits = row_tuple[6]
                row.four_credits = row_tuple[7]
                row.semester = row_tuple[8]
                row.year = row_tuple[9]
                row.application_due = row_tuple[10]
                row.active = row_tuple[11]
                row.last_updated = row_tuple[12]
                row.location = row_tuple[13]

                db.session.add(row)
                db.session.commit()

            courses_rows = (
                ("CSCI2300", "Introduction to Algorithms"),
                ("CSCI4430", "Programming Languages"),
                ("CSCI2961", "Rensselaer Center for Open Source"),
                ("CSCI4390", "Data Mining"),
            )

            for row_tuple in courses_rows:
                row = Courses()
                row.code = row_tuple[0]
                row.name = row_tuple[1]

                db.session.add(row)
                db.session.commit()

            majors_rows = (
                ("CSCI", "Computer Science"),
                ("ECSE", "Electrical, Computer, and Systems Engineering"),
                ("BIOL", "Biological Science"),
                ("MATH", "Mathematics"),
                ("COGS", "Cognitive Science"),
                ("PHYS", "Physics"),
            )

            for row_tuple in majors_rows:
                row = Majors()
                row.code = row_tuple[0]
                row.name = row_tuple[1]

                db.session.add(row)
                db.session.commit()

            # https://www.geeksforgeeks.org/datetime-timezone-in-sqlalchemy/
            # https://www.tutorialspoint.com/handling-timezone-in-python

            leads_rows = (
                (2, 1),
                (1, 1),
                (2, 2),
                (1, 3),
                (4, 4),
                (8, 5),
            )

            for r in leads_rows:
                row = Leads()
                row.lab_manager_id = r[0]
                row.opportunity_id = r[1]

                db.session.add(row)
                db.session.commit()

            recommends_courses_rows = (
                (1, "CSCI4430"),
                (1, "CSCI2961"),
                (2, "CSCI4390"),
            )

            for r in recommends_courses_rows:
                row = RecommendsCourses()
                row.opportunity_id = r[0]
                row.course_code = r[1]

                db.session.add(row)
                db.session.commit()

            recommends_majors_rows = ((1, "CSCI"), (1, "PHYS"), (2, "BIOL"))

            for r in recommends_majors_rows:
                row = RecommendsMajors()
                row.opportunity_id = r[0]
                row.major_code = r[1]

                db.session.add(row)
                db.session.commit()

            recommends_class_years_rows = ((3, 2025), (2, 2025), (2, 2026), (1, 2027))

            for r in recommends_class_years_rows:
                row = RecommendsClassYears()
                row.opportunity_id = r[0]
                row.class_year = r[1]

                db.session.add(row)
                db.session.commit()

            user_majors = (
                ("cenzar", "MATH"),
                ("cenzar", "CSCI"),
                ("test", "CSCI"),
            )

            for r in user_majors:
                row = UserMajors()
                row.user_id = r[0]
                row.major_code = r[1]

                db.session.add(row)
                db.session.commit()

            for r in user_majors:
                row = UserDepartments()
                row.user_id = r[0]
                row.department_id = r[1]

                db.session.add(row)
                db.session.commit()

            user_courses = (
                ("cenzar", "CSCI2300", False),
                ("cenzar", "CSCI4430", True),
                ("test", "CSCI2300", False),
            )

            for r in user_courses:
                row = UserCourses()
                row.user_id = r[0]
                row.course_code = r[1]
                row.in_progress = r[2]

                db.session.add(row)
                db.session.commit()

            participates_rows = (
                ("cenzar", 1),
                ("cenzar", 2),
                ("test", 3),
                ("test", 4),
            )

            for r in participates_rows:
                row = Participates()
                row.user_id = r[0]
                row.opportunity_id = r[1]

                db.session.add(row)
                db.session.commit()

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
            ]

            for table in tables:
                stmt = db.select(table)
                result = db.session.execute(stmt).scalars()

                inst = db.inspect(table)
                attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]

                print(f"{table.__tablename__}")
                print(attr_names)
                for row in result:
                    print(row)
                print()

            print("Number of tables:", len(tables))


if __name__ == "__main__":
    main()
