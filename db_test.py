"""
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable

In sqlalchemy, build queries with the Executable class. (Builder design pattern)
Then pass an Executable into Session.execute()
"""

import sys
import random
import pytz
from datetime import datetime, date, timezone

from sqlalchemy import select

from labconnect import create_app, db
from labconnect.models import *

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
        	("Humanities, Arts and Social Sciences", "also pretty cool")
        ]

        for row_tuple in rpi_departments_rows: 
            row = RPIDepartments(
                name=row_tuple[0],
                description=row_tuple[1],
            )
            db.session.add(row)
            db.session.commit()

        contact_links_rows = [
            ("www.abc.com", "abc company"),
            ("www.discord.com", "discord main page")
        ]

        for row_tuple in contact_links_rows: 
            row = ContactLinks(
                contact_link=row_tuple[0],
                contact_type=row_tuple[1],
            )
            db.session.add(row)
            db.session.commit()

        lab_runner_rows = [
            ("led", "Duy Le"),
            ("cenzar", "Rafael")
        ]

        for row_tuple in lab_runner_rows: 
            row = LabRunner(
                rcs_id=row_tuple[0],
                name=row_tuple[1],
            )
            db.session.add(row)
            db.session.commit()
        
        opportunities_rows = [
            ("Automated Cooling System", "Energy efficient AC system", True, "Thermodynamics"),
            ("Iphone 15 durability test", "Scratching the Iphone, drop testing etc.", True, "Experienced in getting angry and throwing temper tantrum"),
        ]

        for row_tuple in opportunities_rows:
            row = Opportunities(
                name=row_tuple[0],
                description=row_tuple[1],
                active_status=row_tuple[2],
                recommended_experience=row_tuple[3]
            )
            db.session.add(row)
            db.session.commit()

        courses_rows = [
            ("CSCI4430", "Programming Languages"),
            ("CSCI2961", "Rensselaer Center for Open Source"),
            ("CSCI4390", "Data Mining"),
        ]

        for row_tuple in courses_rows:
            row = Courses(
                course_code=row_tuple[0],
                course_name=row_tuple[1]
            )
            db.session.add(row)
            db.session.commit()

        majors_rows = [
            ("CSCI", "Computer Science"),
            ("ECSE", "Electrical, Computer, and Systems Engineering"),
            ("BIOL", "Biological Science"),
            ("MATH", "Mathematics"),
            ("COGS", "Cognitive Science")
        ]
        
        for row_tuple in majors_rows:
            row = Majors(
                major_code=row_tuple[0],
                major_name=row_tuple[1]
            )
            db.session.add(row)
            db.session.commit()

        class_years_rows = [
            (1, "Freshman"),
            (2, "Sophomore"),
            (3, "Junior"),
            (4, "Senior"),
            (5, "Graduate")
        ]

        for row_tuple in class_years_rows:
            row = ClassYears(
                class_year=row_tuple[0],
                class_name=row_tuple[1],
            )
            db.session.add(row)
            db.session.commit()

        # https://www.geeksforgeeks.org/datetime-timezone-in-sqlalchemy/
        # https://www.tutorialspoint.com/handling-timezone-in-python
        
        UTC_TZ = pytz.timezone("UTC")
        app_due_dates_rows = [
            datetime(year=2023, month=10, day=24, hour=16, minute=30, tzinfo=UTC_TZ),
            datetime(year=2024, month=1, day=8, hour=6, minute=30, tzinfo=UTC_TZ),
            datetime(year=2025, month=12, day=20, hour=5, minute=40, tzinfo=UTC_TZ)
        ]

        for app_due_dates_row in app_due_dates_rows:
            row = ApplicationDueDates(
                date = app_due_dates_row
            )
            db.session.add(row)
            db.session.commit()        

        semester_rows = [
            (2024, "Fall"),
            (2023, "Fall"),
            (3024, "Spring")
        ]
        for semester_tuple in semester_rows:
            row = Semesters(
                year=semester_tuple[0],
                season=semester_tuple[1]
            )
            db.session.add(row)
            db.session.commit()

        rows = [15.5, 20, 18.75]
        for r in rows:
            row = SalaryCompInfo(usd_per_hour=r)
            db.session.add(row)
            db.session.commit()

        rows = [9000, 15000, 500, 2500]
        for r in rows:
            row = UpfrontPayCompInfo(usd = r)
            db.session.add(row)
            db.session.commit()

        rows = [
            (4, "CSCI4430"),
            (3, "CSCI2961"),
            (2, "CSCI4430"),
            (1, "CSCI1000")
        ]
        for r in rows:
            row = CreditCompInfo(
                number_of_credits=r[0],
                course_code=r[1]
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
        ]

        for table in tables:

            stmt = select(table)
            result = db.session.execute(stmt)
        
            print(f"{table.__tablename__} rows:")
            for row in result.scalars():
                print(row)
            print()
        
