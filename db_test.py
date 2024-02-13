"""
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable

In sqlalchemy, build queries with the Executable class. (Builder design pattern)
Then pass an Executable into Session.execute()
"""

import sys
from datetime import date

from sqlalchemy import inspect, select

from labconnect import create_app, db
from labconnect.helpers import SemesterEnum
from labconnect.models import (
    ClassYears,
    Courses,
    DepartmentOf,
    IsPartOf,
    LabManager,
    Majors,
    Opportunities,
    Promotes,
    RecommendsClassYears,
    RecommendsCourses,
    RecommendsMajors,
    RPIDepartments,
    RPISchools,
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
            ("Computer Science", "the coolest of them all"),
            ("Materials Engineering", "also pretty cool"),
        )

        for row_tuple in rpi_departments_rows:
            row = RPIDepartments(name=row_tuple[0], description=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        lab_manager_rows = (("led", "Duy Le"), ("cenzar", "Rafael"))

        for row_tuple in lab_manager_rows:
            row = LabManager(rcs_id=row_tuple[0], name=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        opportunities_rows = (
            (
                "Automated Cooling System",
                "Energy efficient AC system",
                "Thermodynamics",
                15.0,
                "4",
                SemesterEnum.SPRING,
                2024,
                date.today(),
            ),
            (
                "Iphone 15 durability test",
                "Scratching the Iphone, drop testing etc.",
                "Experienced in getting angry and throwing temper tantrum",
                None,
                "1,2,3,4",
                SemesterEnum.SPRING,
                2024,
                date.today(),
            ),
        )

        for row_tuple in opportunities_rows:
            row = Opportunities(
                name=row_tuple[0],
                description=row_tuple[1],
                recommended_experience=row_tuple[2],
                pay=row_tuple[3],
                credits=row_tuple[4],
                semester=row_tuple[5],
                year=row_tuple[6],
                application_due=row_tuple[7],
            )
            db.session.add(row)
            db.session.commit()

        courses_rows = (
            ("CSCI4430","Programming Languages"),
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
        )

        for row_tuple in majors_rows:
            row = Majors(major_code=row_tuple[0], major_name=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        class_years_rows = (2024, 2025, 2026, 2027, 2028, 2029)

        for row_item in class_years_rows:
            row = ClassYears(class_year=row_item)
            db.session.add(row)
            db.session.commit()

        # https://www.geeksforgeeks.org/datetime-timezone-in-sqlalchemy/
        # https://www.tutorialspoint.com/handling-timezone-in-python

        is_department_of_rows_schools = (
            ("School of Science", "Computer Science"),
            ("School of Engineering", "Materials Engineering"),
        )

        for r in is_department_of_rows_schools:
            row = DepartmentOf(department_name=r[0], school_name=r[1])
            db.session.add(row)
            db.session.commit()

        is_part_of_rows_lab_managers = (
            ("led", "Computer Science"),
            ("led", "Humanities, Arts and Social Sciences"),
            ("cenzar", "Computer Science"),
        )

        for r in is_part_of_rows_lab_managers:
            row = IsPartOf(lab_manager_rcs_id=r[0], department_name=r[1])
            db.session.add(row)
            db.session.commit()

        promotes_rows = (("led", 1), ("led", 2), ("cenzar", 1), ("cenzar", 2))

        for r in promotes_rows:
            row = Promotes(lab_manager_rcs_id=r[0], opportunity_id=r[1])
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

        recommends_class_years_rows = ((2, 4), (2, 3), (2, 1), (1, 3))

        for r in recommends_class_years_rows:
            row = RecommendsClassYears(opportunity_id=r[0], class_year=r[1])
            db.session.add(row)
            db.session.commit()

        tables = [
            ClassYears,
            Courses,
            IsPartOf,
            LabManager,
            Majors,
            Opportunities,
            Promotes,
            RecommendsClassYears,
            RecommendsCourses,
            RecommendsMajors,
            RPIDepartments,
            RPISchools,
        ]

        for table in tables:
            stmt = select(table)
            result = db.session.execute(stmt)

            inst = inspect(table)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]

            print(f"{table.__tablename__}")
            print(attr_names)
            for row in result.scalars():
                print(row)
            print()

        print("Number of tables:", len(tables))

"""
https://stackoverflow.com/questions/6039342/how-to-print-all-columns-in-sqlalchemy-orm
"""
