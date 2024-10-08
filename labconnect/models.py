from sqlalchemy import Enum, Index, func, event
from sqlalchemy.dialects.postgresql import TSVECTOR

from labconnect import db
from labconnect.helpers import CustomSerializerMixin, LocationEnum, SemesterEnum

# DD - Entities


class User(db.Model, CustomSerializerMixin):
    __tablename__ = "user"

    serialize_only = (
        "id",
        "email",
        "first_name",
        "last_name",
        "preferred_name",
        "phone_number",
        "website",
        "class_year",
        "lab_manager_id",
    )
    serialize_rules = ()

    id = db.Column(db.String(9), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(200), nullable=False, unique=False)
    preferred_name = db.Column(db.String(50), nullable=True, unique=False)
    phone_number = db.Column(db.String(15), nullable=True, unique=False)
    website = db.Column(db.String(512), nullable=True, unique=False)
    class_year = db.Column(
        db.Integer,
        db.ForeignKey("class_years.class_year"),
        nullable=True,
        unique=False,
    )
    lab_manager_id = db.Column(
        db.Integer,
        db.ForeignKey("lab_manager.id"),
        nullable=True,
        unique=False,
    )

    saved_opportunities = db.relationship(
        "UserSavedOpportunities", back_populates="user"
    )
    lab_manager = db.relationship("LabManager", back_populates="user")
    opportunities = db.relationship("Participates", back_populates="user")
    year = db.relationship("ClassYears", back_populates="users")
    departments = db.relationship("UserDepartments", back_populates="user")
    majors = db.relationship("UserMajors", back_populates="user")
    courses = db.relationship("UserCourses", back_populates="user")

    def getLabManager(self):
        return self.lab_manager

    def __repr__(self):
        return f"<User {self.id}>"

    def __str__(self):
        return f"<User> {self.first_name} {self.last_name}"


class ManagementPermissions(db.Model):
    __tablename__ = "management_permissions"

    user_id = db.Column(
        db.String(9), db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    super_admin = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    moderator = db.Column(db.Boolean, nullable=False, default=False)


# lab_manager( id, name ), key: id
class LabManager(db.Model, CustomSerializerMixin):
    __tablename__ = "lab_manager"

    serialize_only = ("id", "department_id")
    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(db.String(64), db.ForeignKey("rpi_departments.name"))

    user = db.relationship("User", back_populates="lab_manager")
    department = db.relationship("RPIDepartments", back_populates="lab_managers")
    opportunities = db.relationship(
        "Leads", back_populates="lab_manager", passive_deletes=True
    )

    def getUser(self):
        return User.query.filter_by(lab_manager_id=self.id).all()

    def getName(self):
        return self.user[0].first_name + " " + self.user[0].last_name

    def getEmail(self):
        return self.user[0].email


# rpi_schools( name, description ), key: name
class RPISchools(db.Model, CustomSerializerMixin):
    __tablename__ = "rpi_schools"

    serialize_only = ("name", "description")
    serialize_rules = ()

    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(2000), nullable=True, unique=False)

    departments = db.relationship("RPIDepartments", back_populates="school")


# rpi_departments( name, description ), key: name
class RPIDepartments(db.Model, CustomSerializerMixin):
    __tablename__ = "rpi_departments"

    serialize_only = ("name", "description", "school_id")
    serialize_rules = ()

    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(2000), nullable=True, unique=False)
    school_id = db.Column(db.String(64), db.ForeignKey("rpi_schools.name"))

    school = db.relationship("RPISchools", back_populates="departments")
    lab_managers = db.relationship("LabManager", back_populates="department")
    users = db.relationship("UserDepartments", back_populates="department")


# opportunities( id, name, description, active_status, recommended_experience ), key: id
class Opportunities(db.Model, CustomSerializerMixin):
    __tablename__ = "opportunities"

    serialize_only = (
        "id",
        "name",
        "description",
        "recommended_experience",
        "pay",
        "one_credit",
        "two_credits",
        "three_credits",
        "four_credits",
        "semester",
        "year",
        "application_due",
        "active",
        "last_updated",
        "location",
    )
    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=True, unique=False)
    description = db.Column(db.String(2000), nullable=True, unique=False)
    recommended_experience = db.Column(db.String(500), nullable=True, unique=False)
    pay = db.Column(db.Float, nullable=True, unique=False)
    one_credit = db.Column(db.Boolean, nullable=True, unique=False)
    two_credits = db.Column(db.Boolean, nullable=True, unique=False)
    three_credits = db.Column(db.Boolean, nullable=True, unique=False)
    four_credits = db.Column(db.Boolean, nullable=True, unique=False)
    semester = db.Column(Enum(SemesterEnum), nullable=True, unique=False)
    year = db.Column(db.Integer, nullable=True, unique=False)
    application_due = db.Column(db.Date, nullable=True, unique=False)
    active = db.Column(db.Boolean, nullable=False, unique=False)
    last_updated = db.Column(db.DateTime, nullable=True, unique=False)
    location = db.Column(Enum(LocationEnum), nullable=True, unique=False)

    lab_managers = db.relationship(
        "Leads", back_populates="opportunity", passive_deletes=True
    )
    users = db.relationship(
        "Participates", back_populates="opportunity", passive_deletes=True
    )
    courses = db.relationship(
        "RecommendsCourses", back_populates="opportunity", passive_deletes=True
    )
    recommends_majors = db.relationship(
        "RecommendsMajors", back_populates="opportunity", passive_deletes=True
    )
    recommends_class_years = db.relationship(
        "RecommendsClassYears", back_populates="opportunity", passive_deletes=True
    )
    saved_opportunities = db.relationship(
        "UserSavedOpportunities", back_populates="opportunity", passive_deletes=True
    )

    # Search Vector
    search_vector = db.Column(TSVECTOR)

    __table_args__ = (
        Index("ix_opportunity_search_vector", search_vector, postgresql_using="gin"),
    )


@event.listens_for(Opportunities, "before_insert")
@event.listens_for(Opportunities, "before_update")
def update_search_vector(_unusedmapper, _unusedconnection, target):
    target.search_vector = func.to_tsvector(
        "english", target.name + " " + target.description
    )


# courses( course_code, course_name ), key: course_code
class Courses(db.Model, CustomSerializerMixin):
    __tablename__ = "courses"

    serialize_only = ("code", "name")
    serialize_rules = ()

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(128), nullable=True, unique=False)

    opportunities = db.relationship(
        "RecommendsCourses", back_populates="course", passive_deletes=True
    )
    users = db.relationship(
        "UserCourses", back_populates="course", passive_deletes=True
    )


# majors( code, name ), key: code
class Majors(db.Model, CustomSerializerMixin):
    __tablename__ = "majors"

    serialize_only = ("code", "name")
    serialize_rules = ()

    code = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=False)

    opportunities = db.relationship(
        "RecommendsMajors", back_populates="major", passive_deletes=True
    )
    users = db.relationship("UserMajors", back_populates="major")


# class_years( class_year ), key: class_year
class ClassYears(db.Model, CustomSerializerMixin):
    __tablename__ = "class_years"

    serialize_only = ("class_year",)
    serialize_rules = ()

    class_year = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)

    opportunities = db.relationship(
        "RecommendsClassYears", back_populates="year", passive_deletes=True
    )
    users = db.relationship("User", back_populates="year")


# DD - Relationships


class UserDepartments(db.Model, CustomSerializerMixin):
    __tablename__ = "user_departments"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    department_id = db.Column(
        db.String(64), db.ForeignKey("rpi_departments.name"), primary_key=True
    )

    user = db.relationship("User", back_populates="departments")
    department = db.relationship("RPIDepartments", back_populates="users")


class UserMajors(db.Model, CustomSerializerMixin):
    __tablename__ = "user_majors"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    major_code = db.Column(db.String(4), db.ForeignKey("majors.code"), primary_key=True)

    user = db.relationship("User", back_populates="majors")
    major = db.relationship("Majors", back_populates="users")


class UserCourses(db.Model, CustomSerializerMixin):
    __tablename__ = "user_courses"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    course_code = db.Column(
        db.String(8), db.ForeignKey("courses.code"), primary_key=True
    )
    in_progress = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="courses")
    course = db.relationship("Courses", back_populates="users")


class UserSavedOpportunities(db.Model):
    __tablename__ = "user_saved_opportunities"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.id"), primary_key=True
    )

    user = db.relationship("User", back_populates="saved_opportunities")
    opportunity = db.relationship("Opportunities", back_populates="saved_opportunities")


class Leads(db.Model):
    __tablename__ = "leads"

    serialize_only = ("lab_manager_id", "opportunity_id")
    serialize_rules = ()

    lab_manager_id = db.Column(
        db.Integer,
        db.ForeignKey("lab_manager.id", ondelete="CASCADE"),
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

    lab_manager = db.relationship("LabManager", back_populates="opportunities")
    opportunity = db.relationship("Opportunities", back_populates="lab_managers")


class Participates(db.Model):
    __tablename__ = "participates"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.id"), primary_key=True
    )

    user = db.relationship("User", back_populates="opportunities")
    opportunity = db.relationship("Opportunities", back_populates="users")


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

    opportunity = db.relationship("Opportunities", back_populates="courses")
    course = db.relationship("Courses", back_populates="opportunities")


class RecommendsMajors(db.Model):
    __tablename__ = "recommends_majors"

    opportunity_id = db.Column(
        db.Integer,
        db.ForeignKey("opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    )
    major_code = db.Column(
        db.String(4),
        db.ForeignKey("majors.code", ondelete="CASCADE"),
        primary_key=True,
    )

    opportunity = db.relationship("Opportunities", back_populates="recommends_majors")
    major = db.relationship("Majors", back_populates="opportunities")


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

    opportunity = db.relationship(
        "Opportunities", back_populates="recommends_class_years"
    )
    year = db.relationship("ClassYears", back_populates="opportunities")
