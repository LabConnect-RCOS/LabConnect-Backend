"""
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable

In sqlalchemy, build queries with the Executable class. (Builder design pattern)
Then pass an Executable into Session.execute()
"""

import sys
from datetime import date, datetime

from labconnect import create_app, db
from labconnect.helpers import LocationEnum, SemesterEnum
from labconnect.models import LabManager  # Professors and Grad students
from labconnect.models import (
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
)

app = create_app()

if len(sys.argv) < 2:
    sys.exit("No argument or exsisting argument found")

if sys.argv[1] == "clear":
    with app.app_context():
        db.drop_all()

elif sys.argv[1] == "create":
    with app.app_context():
        db.create_all()

        rpi_schools_rows = (
            ("School of Science", "the coolest of them all"),
            ("School of Engineering", "also pretty cool"),
        )

        for row_tuple in rpi_schools_rows:
            row = RPISchools(name=row_tuple[0], description=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        rpi_departments_rows = (
            ("Computer Science", "DS", "School of Science"),
            ("Biology", "life", "School of Science"),
            ("Materials Engineering", "also pretty cool", "School of Engineering"),
            ("Environmental Engineering", "water", "School of Engineering"),
            ("Math", "quick maths", "School of Science"),
            (
                "Aerospace Engineering",
                "space, the final frontier",
                "School of Engineering",
            ),
            (
                "Aeronautical Engineering",
                "flying, need for speed",
                "School of Engineering",
            ),
            (
                "Material Science",
                "Creating the best materials",
                "School of Engineering",
            ),
        )

        for row_tuple in rpi_departments_rows:
            row = RPIDepartments(
                name=row_tuple[0], description=row_tuple[1], school_id=row_tuple[2]
            )
            db.session.add(row)
            db.session.commit()

        class_years_rows = (2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031)

        for row_item in class_years_rows:
            row = ClassYears(class_year=row_item, active=True)
            db.session.add(row)
            db.session.commit()

        lab_manager_rows = (
            ("led", "Duy", "Le", "Computer Science"),
            ("turner", "Wes", "Turner", "Computer Science"),
            ("kuzmin", "Konstantine", "Kuzmin", "Computer Science"),
            ("goldd", "David", "Goldschmidt", "Computer Science"),
            ("rami", "Rami", "Rami", "Material Science"),
            ("holm", "Mark", "Holmes", "Math"),
        )

        raf_test_user = (
            "cenzar",
            "Rafael",
            "Cenzano",
            "Raf",
            2025,
            "Computer Science",
        )

        lab_manager = LabManager(department_id=raf_test_user[5])

        db.session.add(lab_manager)
        db.session.commit()

        user = User(
            id=raf_test_user[0],
            email=raf_test_user[0] + "@rpi.edu",
            first_name=raf_test_user[1],
            last_name=raf_test_user[2],
            preferred_name=raf_test_user[3],
            class_year=raf_test_user[4],
            lab_manager_id=lab_manager.id,
        )

        db.session.add(user)
        db.session.commit()

        for row_tuple in lab_manager_rows:
            lab_manager = LabManager(department_id=row_tuple[3])

            db.session.add(lab_manager)
            db.session.commit()

            user = User(
                id=row_tuple[0],
                email=row_tuple[0] + "@rpi.edu",
                first_name=row_tuple[1],
                last_name=row_tuple[2],
                lab_manager_id=lab_manager.id,
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
                2024,
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
                2024,
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
                2024,
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
                2024,
                date.today(),
                True,
                datetime.now(),
                LocationEnum.JEC,
            ),
        )

        for row_tuple in opportunities_rows:
            row = Opportunities(
                name=row_tuple[0],
                description=row_tuple[1],
                recommended_experience=row_tuple[2],
                pay=row_tuple[3],
                one_credit=row_tuple[4],
                two_credits=row_tuple[5],
                three_credits=row_tuple[6],
                four_credits=row_tuple[7],
                semester=row_tuple[8],
                year=row_tuple[9],
                application_due=row_tuple[10],
                active=row_tuple[11],
                last_updated=row_tuple[12],
                location=row_tuple[13],
            )
            db.session.add(row)
            db.session.commit()

        courses_rows = (
            ("CSCI2300", "Introduction to Algorithms"),
            ("CSCI4430", "Programming Languages"),
            ("CSCI2961", "Rensselaer Center for Open Source"),
            ("CSCI4390", "Data Mining"),
        )

        for row_tuple in courses_rows:
            row = Courses(code=row_tuple[0], name=row_tuple[1])
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
            row = Majors(code=row_tuple[0], name=row_tuple[1])
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
        )

        for r in leads_rows:
            row = Leads(lab_manager_id=r[0], opportunity_id=r[1])
            db.session.add(row)
            db.session.commit()

        recommends_courses_rows = ((1, "CSCI4430"), (1, "CSCI2961"), (2, "CSCI4390"))

        for r in recommends_courses_rows:
            row = RecommendsCourses(opportunity_id=r[0], course_code=r[1])
            db.session.add(row)
            db.session.commit()

        recommends_majors_rows = ((1, "CSCI"), (1, "PHYS"), (2, "BIOL"))

        for r in recommends_majors_rows:
            row = RecommendsMajors(opportunity_id=r[0], major_code=r[1])
            db.session.add(row)
            db.session.commit()

        recommends_class_years_rows = ((2, 2024), (2, 2025), (2, 2026), (1, 2027))

        for r in recommends_class_years_rows:
            row = RecommendsClassYears(opportunity_id=r[0], class_year=r[1])
            db.session.add(row)
            db.session.commit()

        user_rows = (
            (
                "test",
                "test@rpi.edu",
                "RCOS",
                "RCOS",
                None,
                2028,
            ),
            (
                "test2",
                "test2@rpi.edu",
                "RCOS",
                "RCOS",
                None,
                2029,
            ),
            (
                "test3",
                "test3@rpi.edu",
                "RCOS",
                "RCOS",
                None,
                2025,
            ),
        )
        for r in user_rows:
            row = User(
                id=r[0],
                email=r[1],
                first_name=r[2],
                last_name=r[3],
                preferred_name=r[4],
                class_year=r[5],
            )
            db.session.add(row)
            db.session.commit()

        user_majors = (
            ("cenzar", "MATH"),
            ("cenzar", "CSCI"),
            ("test", "CSCI"),
        )

        for r in user_majors:
            row = UserMajors(user_id=r[0], major_code=r[1])
            db.session.add(row)
            db.session.commit()

        user_departments = (
            ("cenzar", "Computer Science"),
            ("cenzar", "Math"),
            ("test", "Computer Science"),
        )

        for r in user_departments:
            row = UserDepartments(user_id=r[0], department_id=r[1])
            db.session.add(row)
            db.session.commit()

        user_courses = (
            ("cenzar", "CSCI2300", False),
            ("cenzar", "CSCI4430", True),
            ("test", "CSCI2300", False),
        )

        for r in user_courses:
            row = UserCourses(user_id=r[0], course_code=r[1], in_progress=r[2])
            db.session.add(row)
            db.session.commit()

        participates_rows = (
            ("cenzar", 1),
            ("cenzar", 2),
            ("test", 3),
            ("test", 4),
        )

        for r in participates_rows:
            row = Participates(user_id=r[0], opportunity_id=r[1])
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
