from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from labconnect import db
from labconnect.helpers import CustomSerializerMixin, SemesterEnum, LocationEnum

# DD - Entities


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    class_year = db.Column(
        db.Integer, db.ForeignKey("class_years.class_year"), primary_key=True
    )
    opportunities = relationship("Participates", back_populates="user")

    year = relationship("ClassYears", back_populates="users")
    departments = relationship("UserDepartments", back_populates="user")
    majors = relationship("UserMajors", back_populates="user")


# rpi_schools( name, description ), key: name
class RPISchools(db.Model, CustomSerializerMixin):
    __tablename__ = "rpi_schools"

    serialize_only = ("name", "description")
    serialize_rules = ()

    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(2000), nullable=True, unique=False)

    departments = relationship("RPIDepartments", back_populates="school")


# rpi_departments( name, description ), key: name
class RPIDepartments(db.Model, CustomSerializerMixin):
    __tablename__ = "rpi_departments"

    serialize_only = ("name", "description")
    serialize_rules = ()

    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(2000), nullable=True, unique=False)

    school_id = db.Column(db.String(64), db.ForeignKey("rpi_schools.name"))

    school = relationship("RPISchools", back_populates="departments")
    lab_managers = relationship("LabManager", back_populates="department")
    users = relationship("UserDepartments", back_populates="department")


# lab_manager( rcs_id, name ), key: rcs_id
class LabManager(db.Model, CustomSerializerMixin):
    __tablename__ = "lab_manager"

    serialize_only = ("rcs_id", "name", "email", "alt_email", "phone_number", "website")
    serialize_rules = ()

    rcs_id = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=False)
    email = db.Column(db.String(64), nullable=True, unique=False)
    alt_email = db.Column(db.String(64), nullable=True, unique=False)
    phone_number = db.Column(db.String(15), nullable=True, unique=False)
    website = db.Column(db.String(128), nullable=True, unique=False)

    department_id = db.Column(db.String(64), db.ForeignKey("rpi_departments.name"))

    department = relationship("RPIDepartments", back_populates="lab_managers")
    opportunities = relationship(
        "Leads", back_populates="lab_manager", passive_deletes=True
    )


# opportunities( id, name, description, active_status, recommended_experience ), key: id
class Opportunities(db.Model, CustomSerializerMixin):
    __tablename__ = "opportunities"

    serialize_only = (
        "id",
        "name",
        "description",
        "recommended_experience",
        "pay",
        "credits",
        "semester",
        "year",
        "application_due",
        "active",
    )
    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=True, unique=False)
    description = db.Column(db.String(2000), nullable=True, unique=False)
    recommended_experience = db.Column(db.String(500), nullable=True, unique=False)
    pay = db.Column(db.Float, nullable=True, unique=False)
    credits = db.Column(db.String(8), nullable=True, unique=False)
    semester = db.Column(Enum(SemesterEnum), nullable=True, unique=False)
    year = db.Column(db.Integer, nullable=True, unique=False)
    application_due = db.Column(db.Date, nullable=True, unique=False)
    active = db.Column(db.Boolean, nullable=False, unique=False)
    last_updated = db.Column(db.DateTime, nullable=True, unique=False)
    location = db.Column(Enum(LocationEnum), nullable=True, unique=False)

    lab_managers = relationship(
        "Leads", back_populates="opportunity", passive_deletes=True
    )
    users = relationship(
        "Participates", back_populates="opportunity", passive_deletes=True
    )
    courses = relationship(
        "RecommendsCourses", back_populates="opportunity", passive_deletes=True
    )
    recommends_majors = relationship(
        "RecommendsMajors", back_populates="opportunity", passive_deletes=True
    )
    recommends_class_years = relationship(
        "RecommendsClassYears", back_populates="opportunity", passive_deletes=True
    )


# courses( course_code, course_name ), key: course_code
class Courses(db.Model, CustomSerializerMixin):
    __tablename__ = "courses"

    serialize_only = ("code", "name")
    serialize_rules = ()

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(128), nullable=True, unique=False)

    opportunities = relationship(
        "RecommendsCourses", back_populates="course", passive_deletes=True
    )


# majors( code, name ), key: code
class Majors(db.Model, CustomSerializerMixin):
    __tablename__ = "majors"

    serialize_only = ("code", "name")
    serialize_rules = ()

    code = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=False)

    opportunities = relationship(
        "RecommendsMajors", back_populates="major", passive_deletes=True
    )
    users = relationship("UserMajors", back_populates="major")


# class_years( class_year ), key: class_year
class ClassYears(db.Model, CustomSerializerMixin):
    __tablename__ = "class_years"

    serialize_only = ("class_year",)
    serialize_rules = ()

    class_year = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)

    opportunities = relationship(
        "RecommendsClassYears", back_populates="year", passive_deletes=True
    )
    users = relationship("User", back_populates="year")


# DD - Relationships


# leads( lab_manager_rcs_id, opportunity_id ), key: (lab_manager_rcs_id, opportunity_id)
class UserDepartments(db.Model):
    __tablename__ = "user_departments"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    department_id = db.Column(
        db.Integer, db.ForeignKey("rpi_departments.name"), primary_key=True
    )

    user = relationship("User", back_populates="departments")
    department = relationship("RPIDepartments", back_populates="users")


# leads( lab_manager_rcs_id, opportunity_id ), key: (lab_manager_rcs_id, opportunity_id)
class UserMajors(db.Model):
    __tablename__ = "user_majors"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    major_code = db.Column(db.Integer, db.ForeignKey("majors.code"), primary_key=True)

    user = relationship("User", back_populates="majors")
    major = relationship("Majors", back_populates="users")


# leads( lab_manager_rcs_id, opportunity_id ), key: (lab_manager_rcs_id, opportunity_id)
class Leads(db.Model):
    __tablename__ = "leads"

    lab_manager_rcs_id = db.Column(
        db.String(9),
        db.ForeignKey("lab_manager.rcs_id", ondelete="CASCADE"),
        primary_key=True,
    )
    opportunity_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "opportunities.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    lab_manager = relationship("LabManager", back_populates="opportunities")
    opportunity = relationship("Opportunities", back_populates="lab_managers")


# participates( user_id, opportunity_id ), key: (user_id, opportunity_id)
class Participates(db.Model):
    __tablename__ = "participates"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.id"), primary_key=True
    )

    user = relationship("User", back_populates="opportunities")
    opportunity = relationship("Opportunities", back_populates="users")


# recommends_courses( opportunity_id, course_code ), key: (opportunity_id, course_code)
class RecommendsCourses(db.Model):
    __tablename__ = "recommends_courses"

    opportunity_id = db.Column(
        db.Integer,
        db.ForeignKey("opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    )
    course_code = db.Column(
        db.String(8),
        db.ForeignKey("courses.code", ondelete="CASCADE"),
        primary_key=True,
    )

    opportunity = relationship("Opportunities", back_populates="courses")
    course = relationship("Courses", back_populates="opportunities")


# recommends_majors( opportunity_id, code ), key: (opportunity_id, code)
class RecommendsMajors(db.Model):
    __tablename__ = "recommends_majors"

    opportunity_id = db.Column(
        db.Integer,
        db.ForeignKey("opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    )
    major_code = db.Column(
        db.String(8),
        db.ForeignKey("majors.code", ondelete="CASCADE"),
        primary_key=True,
    )

    opportunity = relationship("Opportunities", back_populates="recommends_majors")
    major = relationship("Majors", back_populates="opportunities")


# recommends_c_years( opportunity_id, class_year ), key: (opportunity_id, class_year)
class RecommendsClassYears(db.Model):
    __tablename__ = "recommends_class_years"

    opportunity_id = db.Column(
        db.Integer,
        db.ForeignKey("opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    )
    class_year = db.Column(
        db.Integer,
        db.ForeignKey("class_years.class_year", ondelete="CASCADE"),
        primary_key=True,
    )

    opportunity = relationship("Opportunities", back_populates="recommends_class_years")
    year = relationship("ClassYears", back_populates="opportunities")


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
