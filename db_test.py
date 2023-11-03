"""
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable

In sqlalchemy, build queries with the Executable class. (Builder design pattern)
Then pass an Executable into Session.execute()
"""

import sys
from datetime import datetime

import pytz
from sqlalchemy import inspect, select

from labconnect import create_app, db
from labconnect.models import (
    RPIDepartments,
    ContactLinks,
    LabRunner,
    Opportunities,
    Courses,
    Majors,
    ClassYears,
    ApplicationDueDates,
    Semesters,
    SalaryCompInfo,
    UpfrontPayCompInfo,
    CreditCompInfo,
    IsPartOf,
    HasLink,
    Promotes,
    RecommendsCourses,
    RecommendsMajors,
    RecommendsClassYears,
    ApplicationDue,
    ActiveSemesters,
    HasSalaryComp,
    HasUpfrontPayComp,
    HasCreditComp,
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

        rpi_departments_rows = [
            ("Computer Science", "the coolest of them all"),
            ("Humanities, Arts and Social Sciences", "also pretty cool"),
        ]

        for row_tuple in rpi_departments_rows:
            row = RPIDepartments(name=row_tuple[0], description=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        contact_links_rows = [
            ("www.abc.com", "abc company"),
            ("www.discord.com", "discord main page"),
            ("https://github.com/SabreBirdOne", "Duy Le's Github"),
            ("https://github.com/RafaelCenzano", "Rafael's Github"),
            (
                "https://science.rpi.edu/computer-science",
                "RPI Computer Science Department",
            ),
        ]

        for row_tuple in contact_links_rows:
            row = ContactLinks(contact_link=row_tuple[0], contact_type=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        lab_runner_rows = [("led", "Duy Le"), ("cenzar", "Rafael")]

        for row_tuple in lab_runner_rows:
            row = LabRunner(rcs_id=row_tuple[0], name=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        opportunities_rows = [
            (
                "Automated Cooling System",
                "Energy efficient AC system",
                True,
                "Thermodynamics",
            ),
            (
                "Iphone 15 durability test",
                "Scratching the Iphone, drop testing etc.",
                True,
                "Experienced in getting angry and throwing temper tantrum",
            ),
        ]

        for row_tuple in opportunities_rows:
            row = Opportunities(
                name=row_tuple[0],
                description=row_tuple[1],
                active_status=row_tuple[2],
                recommended_experience=row_tuple[3],
            )
            db.session.add(row)
            db.session.commit()

        courses_rows = [
            ("CSCI4430", "Programming Languages"),
            ("CSCI2961", "Rensselaer Center for Open Source"),
            ("CSCI4390", "Data Mining"),
        ]

        for row_tuple in courses_rows:
            row = Courses(course_code=row_tuple[0], course_name=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        majors_rows = [
            ("CSCI", "Computer Science"),
            ("ECSE", "Electrical, Computer, and Systems Engineering"),
            ("BIOL", "Biological Science"),
            ("MATH", "Mathematics"),
            ("COGS", "Cognitive Science"),
        ]

        for row_tuple in majors_rows:
            row = Majors(major_code=row_tuple[0], major_name=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        class_years_rows = [
            (1, "Freshman"),
            (2, "Sophomore"),
            (3, "Junior"),
            (4, "Senior"),
            (5, "Graduate"),
        ]

        for row_tuple in class_years_rows:
            row = ClassYears(class_year=row_tuple[0], class_name=row_tuple[1])
            db.session.add(row)
            db.session.commit()

        # https://www.geeksforgeeks.org/datetime-timezone-in-sqlalchemy/
        # https://www.tutorialspoint.com/handling-timezone-in-python

        UTC_TZ = pytz.timezone("UTC")
        app_due_dates_rows = [
            datetime(year=2023, month=10, day=24, hour=16, minute=30, tzinfo=UTC_TZ),
            datetime(year=2024, month=1, day=8, hour=6, minute=30, tzinfo=UTC_TZ),
            datetime(year=2025, month=12, day=20, hour=5, minute=40, tzinfo=UTC_TZ),
        ]

        for app_due_dates_row in app_due_dates_rows:
            row = ApplicationDueDates(date=app_due_dates_row)
            db.session.add(row)
            db.session.commit()

        semester_rows = [(2024, "Fall"), (2023, "Fall"), (3024, "Spring")]
        for semester_tuple in semester_rows:
            row = Semesters(year=semester_tuple[0], season=semester_tuple[1])
            db.session.add(row)
            db.session.commit()

        salary_rows = [15.5, 20, 18.75]
        for r in salary_rows:
            row = SalaryCompInfo(usd_per_hour=r)
            db.session.add(row)
            db.session.commit()

        upfront_rows = [9000, 15000, 500, 2500]
        for r in upfront_rows:
            row = UpfrontPayCompInfo(usd=r)
            db.session.add(row)
            db.session.commit()

        credit_comp_rows = [
            (4, "CSCI4430"),
            (3, "CSCI2961"),
            (2, "CSCI4430"),
            (1, "CSCI1000"),
        ]
        for r in credit_comp_rows:
            row = CreditCompInfo(number_of_credits=r[0], course_code=r[1])
            db.session.add(row)
            db.session.commit()

        is_part_of_rows = [
            ("led", "Computer Science"),
            ("led", "Humanities, Arts and Social Sciences"),
            ("cenzar", "Computer Science"),
        ]
        for r in is_part_of_rows:
            row = IsPartOf(lab_runner_rcs_id=r[0], dep_name=r[1])
            db.session.add(row)
            db.session.commit()

        has_link_rows = [
            ("led", "https://github.com/SabreBirdOne"),
            ("led", "https://science.rpi.edu/computer-science"),
            ("cenzar", "https://github.com/RafaelCenzano"),
        ]
        for r in has_link_rows:
            row = HasLink(lab_runner_rcs_id=r[0], contact_link=r[1])
            db.session.add(row)
            db.session.commit()

        promotes_rows = [("led", 1), ("led", 2), ("cenzar", 1), ("cenzar", 2)]
        for r in promotes_rows:
            row = Promotes(lab_runner_rcs_id=r[0], opportunity_id=r[1])
            db.session.add(row)
            db.session.commit()

        recommends_courses_rows = [(1, "CSCI4430"), (1, "CSCI2961"), (2, "CSCI4390")]
        for r in recommends_courses_rows:
            row = RecommendsCourses(opportunity_id=r[0], course_code=r[1])
            db.session.add(row)
            db.session.commit()

        recommends_majors_rows = [(1, "CSCI"), (1, "PHYS"), (2, "BIOL")]
        for r in recommends_majors_rows:
            row = RecommendsMajors(opportunity_id=r[0], major_code=r[1])
            db.session.add(row)
            db.session.commit()

        recommends_class_years_rows = [(2, 4), (2, 3), (2, 1), (1, 3)]
        for r in recommends_class_years_rows:
            row = RecommendsClassYears(opportunity_id=r[0], class_year=r[1])
            db.session.add(row)
            db.session.commit()

        application_due_rows = [  # app_due_dates_rows
            (2, app_due_dates_rows[0]),
            (2, app_due_dates_rows[1]),
            (1, app_due_dates_rows[2]),
        ]
        for r in application_due_rows:
            row = ApplicationDue(opportunity_id=r[0], date=r[1])
            db.session.add(row)
            db.session.commit()

        active_semesters_rows = [  # semester_rows
            (2, semester_rows[0][0], semester_rows[0][1]),
            (2, semester_rows[1][0], semester_rows[1][1]),
            (1, semester_rows[2][0], semester_rows[2][1]),
        ]
        for r in active_semesters_rows:
            row = ActiveSemesters(opportunity_id=r[0], year=r[1], season=r[2])
            db.session.add(row)
            db.session.commit()

        has_salary_comp_rows = [  # salary_rows
            (2, salary_rows[0]),
            (2, salary_rows[1]),
            (1, salary_rows[2]),
        ]
        for r in has_salary_comp_rows:
            row = HasSalaryComp(opportunity_id=r[0], usd_per_hour=r[1])
            db.session.add(row)
            db.session.commit()

        has_upfront_pay_comp_rows = [  # upfront_rows
            (2, upfront_rows[0]),
            (2, upfront_rows[1]),
            (1, upfront_rows[2]),
        ]
        for r in has_upfront_pay_comp_rows:
            row = HasUpfrontPayComp(opportunity_id=r[0], usd=r[1])
            db.session.add(row)
            db.session.commit()

        has_credit_comp_rows = [  # credit_comp_rows
            (2, credit_comp_rows[0][0], credit_comp_rows[0][1]),
            (2, credit_comp_rows[1][0], credit_comp_rows[1][1]),
            (1, credit_comp_rows[2][0], credit_comp_rows[2][1]),
        ]
        for r in has_credit_comp_rows:
            row = HasCreditComp(
                opportunity_id=r[0], number_of_credits=r[1], course_code=r[2]
            )
            db.session.add(row)
            db.session.commit()

        tables = [
            RPIDepartments,
            ContactLinks,
            LabRunner,
            Opportunities,
            Courses,
            Majors,
            ClassYears,
            ApplicationDueDates,
            Semesters,
            SalaryCompInfo,
            UpfrontPayCompInfo,
            CreditCompInfo,
            IsPartOf,
            HasLink,
            Promotes,
            RecommendsCourses,
            RecommendsMajors,
            RecommendsClassYears,
            ApplicationDue,
            ActiveSemesters,
            HasSalaryComp,
            HasUpfrontPayComp,
            HasCreditComp,
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
