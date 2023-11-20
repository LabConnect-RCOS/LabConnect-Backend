from sqlalchemy.orm import relationship

from labconnect import db

# DD - Entities


# rpi_departments( name, description ), key: name
class RPIDepartments(db.Model):
    __tablename__ = "rpi_departments"
    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(256), nullable=True, unique=False)

    lab_runners = relationship(
        "LabRunner", secondary="isPartOf", back_populates="rpi_departments"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.description}"


# contact_links( contact_link, contact_type ), key: contact_link
class ContactLinks(db.Model):
    __tablename__ = "contact_links"
    contact_link = db.Column(db.String(256), primary_key=True)
    contact_type = db.Column(db.String(64), nullable=True, unique=False)

    lab_runners = relationship(
        "LabRunner", secondary="hasLink", back_populates="contact_links"
    )

    def __str__(self) -> str:
        return f"{self.contact_link}, {self.contact_type}"


# lab_runner( rcs_id, name ), key: rcs_id
class LabRunner(db.Model):
    __tablename__ = "lab_runner"
    rcs_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=False)

    rpi_departments = relationship("RPIDepartments", secondary="isPartOf")
    contact_links = relationship("ContactLinks", secondary="hasLink")
    promoted_opportunities = relationship("Opportunities", secondary="promotes")

    def __str__(self) -> str:
        return f"{self.rcs_id}, {self.name}"


# opportunities( id, name, description, active_status, recommended_experience ), key: id
class Opportunities(db.Model):
    __tablename__ = "opportunities"
    opp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=True, unique=False)
    description = db.Column(db.String(256), nullable=True, unique=False)
    active_status = db.Column(db.Boolean, nullable=False, unique=False)
    recommended_experience = db.Column(db.String(256), nullable=True, unique=False)

    lab_runners = relationship(
        "LabRunner", secondary="promotes", back_populates="promoted_opportunities"
    )
    recommends_courses = relationship("Courses", secondary="recommends_courses")
    recommends_majors = relationship("Majors", secondary="recommends_majors")
    recommends_class_years = relationship(
        "ClassYears", secondary="recommends_class_years"
    )
    application_due = relationship("ApplicationDueDates", secondary="application_due")
    active_semesters = relationship("Semesters", secondary="active_semesters")
    has_salary_comp = relationship("SalaryCompInfo", secondary="has_salary_comp")
    has_upfront_pay_comp = relationship(
        "UpfrontPayCompInfo", secondary="has_upfront_pay_comp"
    )
    has_credit_comp = relationship("CreditCompInfo", secondary="has_credit_comp")

    def __str__(self) -> str:
        return f"{self.opp_id}, {self.name}, {self.description}, {self.active_status}, {self.recommended_experience}"


# courses( course_code, course_name ), key: course_code
class Courses(db.Model):
    __tablename__ = "courses"
    course_code = db.Column(db.String(8), primary_key=True)
    course_name = db.Column(db.String(64), nullable=True, unique=False)

    recommended_by_opportunities = relationship(
        "Opportunities",
        secondary="recommends_courses",
        back_populates="recommends_courses",
    )

    def __str__(self) -> str:
        return f"{self.course_code}, {self.course_name}"


# majors( major_code, major_name ), key: major_code
class Majors(db.Model):
    __tablename__ = "majors"
    major_code = db.Column(db.String(4), primary_key=True)
    major_name = db.Column(db.String(64), nullable=True, unique=False)

    recommended_by_opportunities = relationship(
        "Opportunities",
        secondary="recommends_majors",
        back_populates="recommends_majors",
    )

    def __str__(self) -> str:
        return f"{self.major_code}, {self.major_name}"


# class_years( class_year, class_name ), key: class_year
class ClassYears(db.Model):
    __tablename__ = "class_years"
    class_year = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(64), nullable=True, unique=False)

    recommends_class_years = relationship(
        "Opportunities",
        secondary="recommends_class_years",
        back_populates="recommends_class_years",
    )

    def __str__(self) -> str:
        return f"{self.class_year}, {self.class_name}"


# application_due_dates( date ), key: date
class ApplicationDueDates(db.Model):
    __tablename__ = "application_due_dates"
    date = db.Column(db.DateTime(), primary_key=True)

    application_due = relationship(
        "Opportunities", secondary="application_due", back_populates="application_due"
    )

    def __str__(self) -> str:
        return self.date.isoformat()


# semesters( year, season ), key: (year, season)
class Semesters(db.Model):
    __tablename__ = "semesters"
    year = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(64), primary_key=True)

    active_semesters = relationship(
        "Opportunities", secondary="active_semesters", back_populates="active_semesters"
    )

    def __str__(self) -> str:
        return f"{self.year}, {self.season}"


# salary_comp_info( usd_per_hour ), key: usd_per_hour
class SalaryCompInfo(db.Model):
    __tablename__ = "salary_comp_info"
    usd_per_hour = db.Column(db.Float(64), primary_key=True)

    has_salary_comp = relationship(
        "Opportunities", secondary="has_salary_comp", back_populates="has_salary_comp"
    )

    def __str__(self) -> str:
        return f"{self.usd_per_hour}"


# upfront_pay_comp_info( usd ), key: usd
class UpfrontPayCompInfo(db.Model):
    __tablename__ = "upfront_pay_comp_info"
    usd = db.Column(db.Float(64), primary_key=True)

    has_upfront_pay_comp = relationship(
        "Opportunities",
        secondary="has_upfront_pay_comp",
        back_populates="has_upfront_pay_comp",
    )

    def __str__(self) -> str:
        return f"{self.usd}"


# credit_comp_info( number_of_credits, course_code ), key: (number_of_credits, course_code)
class CreditCompInfo(db.Model):
    __tablename__ = "credit_comp_info"
    number_of_credits = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(8), primary_key=True)

    has_credit_comp = relationship(
        "Opportunities", secondary="has_credit_comp", back_populates="has_credit_comp"
    )

    def __str__(self) -> str:
        return f"{self.number_of_credits}, {self.course_code}"


# DD - Relationships


# isPartOf( lab_runner_rcs_id, dep_name ), key: (lab_runner_rcs_id, dep_name)
class IsPartOf(db.Model):
    __tablename__ = "isPartOf"

    lab_runner_rcs_id = db.Column(
        db.String(64), db.ForeignKey("lab_runner.rcs_id"), primary_key=True
    )
    dep_name = db.Column(
        db.String(64), db.ForeignKey("rpi_departments.name"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.lab_runner_rcs_id}, {self.dep_name}"


# hasLink( lab_runner_rcs_id, contact_link ), key: (lab_runner_rcs_id, contact_link)
class HasLink(db.Model):
    __tablename__ = "hasLink"

    lab_runner_rcs_id = db.Column(
        db.String(64), db.ForeignKey("lab_runner.rcs_id"), primary_key=True
    )
    contact_link = db.Column(
        db.String(256), db.ForeignKey("contact_links.contact_link"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.lab_runner_rcs_id}, {self.contact_link}"


# promotes( lab_runner_rcs_id, opportunity_id ), key: (lab_runner_rcs_id, opportunity_id)
class Promotes(db.Model):
    __tablename__ = "promotes"

    lab_runner_rcs_id = db.Column(
        db.String(64), db.ForeignKey("lab_runner.rcs_id"), primary_key=True
    )
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.lab_runner_rcs_id}, {self.opportunity_id}"


# recommends_courses( opportunity_id, course_code ), key: (opportunity_id, course_code)
class RecommendsCourses(db.Model):
    __tablename__ = "recommends_courses"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    course_code = db.Column(
        db.String(8), db.ForeignKey("courses.course_code"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.course_code}"


# recommends_majors( opportunity_id, major_code ), key: (opportunity_id, major_code)
class RecommendsMajors(db.Model):
    __tablename__ = "recommends_majors"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    major_code = db.Column(
        db.String(4), db.ForeignKey("majors.major_code"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.major_code}"


# recommends_c_years( opportunity_id, class_year ), key: (opportunity_id, class_year)
class RecommendsClassYears(db.Model):
    __tablename__ = "recommends_class_years"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    class_year = db.Column(
        db.Integer, db.ForeignKey("class_years.class_year"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.class_year}"


# application_due( opportunity_id, date ), key: (opportunity_id, date)
class ApplicationDue(db.Model):
    __tablename__ = "application_due"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    date = db.Column(
        db.DateTime(), db.ForeignKey("application_due_dates.date"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.date}"


# active_semesters( opportunity_id, year, season ), key: (opportunity_id, year, season)
class ActiveSemesters(db.Model):
    __tablename__ = "active_semesters"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    year = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(64), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["year", "season"], ["semesters.year", "semesters.season"]
        ),
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.year}, {self.season}"


# has_salary_comp( opportunity_id, usd_per_hour ), key: (opportunity_id, usd_per_hour)
class HasSalaryComp(db.Model):
    __tablename__ = "has_salary_comp"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    usd_per_hour = db.Column(
        db.Float(64), db.ForeignKey("salary_comp_info.usd_per_hour"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.usd_per_hour}"


# has_upfront_pay_comp( opportunity_id, usd ), key: (opportunity_id, usd)
class HasUpfrontPayComp(db.Model):
    __tablename__ = "has_upfront_pay_comp"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    usd = db.Column(
        db.Float(64), db.ForeignKey("upfront_pay_comp_info.usd"), primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.usd}"


# has_credit_comp( opportunity_id, number_of_credits, course_code ), key: (opportunity_id, number_of_credits, course_code)
class HasCreditComp(db.Model):
    __tablename__ = "has_credit_comp"

    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.opp_id"), primary_key=True
    )
    number_of_credits = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(8), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["number_of_credits", "course_code"],
            ["credit_comp_info.number_of_credits", "credit_comp_info.course_code"],
        ),
    )

    def __str__(self) -> str:
        return f"{self.opportunity_id}, {self.number_of_credits}, {self.course_code}"


"""

Many-to-many relationships:
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship
https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy#step-2-setting-up-database-models-for-a-many-to-many-relationship
Ben's response: https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example 

Composite foreign keys:
https://stackoverflow.com/questions/7504753/relations-on-composite-keys-using-sqlalchemy
https://avacariu.me/writing/2019/composite-foreign-keys-and-many-to-many-relationships-in-sqlalchemy

Example table in SQLAlchemy

class BacktestClasses(db.Model):
    __tablename__ = "backtest_classes"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    subject_code = db.Column(db.String(4), nullable=False, unique=False)
    course_number = db.Column(db.Integer, nullable=False, unique=False)
    name_of_class = db.Column(db.String(150), nullable=False, unique=False)
    is_alias = db.Column(db.Boolean, nullable=False, unique=False)
    alias_subject_code = db.Column(db.String(4), nullable=True, unique=False)
    alias_course_number = db.Column(db.Integer, nullable=True, unique=False)

    def __str__(self) -> str:
        if self.is_alias:
            return f"(Class: {self.id}, {self.subject_code} {self.course_number} {self.name_of_class}), is alias to {self.alias_subject_code} {self.course_number}"
        return f"(Class: {self.id}, {self.subject_code} {self.course_number} {self.name_of_class})"
"""
