import enum
from datetime import datetime, timezone

from sqlalchemy import Enum, Index, event, func
from sqlalchemy.dialects.postgresql import TSVECTOR

from labconnect import db
from labconnect.helpers import (
    LabManagerTypeEnum,
    LocationEnum,
    SemesterEnum,
)

# DD - Entities


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(9), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(200), nullable=False, unique=False)
    preferred_name = db.Column(db.String(50), nullable=True, unique=False)
    pronouns = db.Column(db.String(25), nullable=True, unique=False)
    phone_number = db.Column(db.String(15), nullable=True, unique=False)
    website = db.Column(db.String(512), nullable=True, unique=False)
    description = db.Column(db.String(4096), nullable=True, unique=False)
    profile_picture = db.Column(db.String(512), nullable=True, unique=False)
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
class LabManager(db.Model):
    __tablename__ = "lab_manager"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager_type = db.Column(Enum(LabManagerTypeEnum), nullable=True, unique=False)
    department_id = db.Column(db.String(4), db.ForeignKey("rpi_departments.id"))

    user = db.relationship("User", back_populates="lab_manager")
    department = db.relationship("RPIDepartments", back_populates="lab_managers")
    opportunities = db.relationship(
        "Leads", back_populates="lab_manager", passive_deletes=True
    )


# rpi_schools( name, description ), key: name
class RPISchools(db.Model):
    __tablename__ = "rpi_schools"

    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(2000), nullable=True, unique=False)

    departments = db.relationship("RPIDepartments", back_populates="school")


# rpi_departments( name, description ), key: name
class RPIDepartments(db.Model):
    __tablename__ = "rpi_departments"

    id = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=False)
    image = db.Column(db.String(512), nullable=True, unique=False)
    description = db.Column(db.String(2000), nullable=True, unique=False)
    website = db.Column(db.String(512), nullable=True, unique=False)
    school_id = db.Column(db.String(64), db.ForeignKey("rpi_schools.name"))

    school = db.relationship("RPISchools", back_populates="departments")
    lab_managers = db.relationship("LabManager", back_populates="department")
    users = db.relationship("UserDepartments", back_populates="department")


# opportunities( id, name, description, active_status, recommended_experience ), key: id
class Opportunities(db.Model):
    __tablename__ = "opportunities"

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
class Courses(db.Model):
    __tablename__ = "courses"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(128), nullable=True, unique=False)

    opportunities = db.relationship(
        "RecommendsCourses", back_populates="course", passive_deletes=True
    )
    users = db.relationship(
        "UserCourses", back_populates="course", passive_deletes=True
    )


# majors( code, name ), key: code
class Majors(db.Model):
    __tablename__ = "majors"

    code = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=False)

    opportunities = db.relationship(
        "RecommendsMajors", back_populates="major", passive_deletes=True
    )
    users = db.relationship("UserMajors", back_populates="major")


# class_years( class_year ), key: class_year
class ClassYears(db.Model):
    __tablename__ = "class_years"

    class_year = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)

    opportunities = db.relationship(
        "RecommendsClassYears", back_populates="year", passive_deletes=True
    )
    users = db.relationship("User", back_populates="year")


# DD - Relationships


class UserDepartments(db.Model):
    __tablename__ = "user_departments"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    department_id = db.Column(
        db.String(4), db.ForeignKey("rpi_departments.id"), primary_key=True
    )

    user = db.relationship("User", back_populates="departments")
    department = db.relationship("RPIDepartments", back_populates="users")


class UserMajors(db.Model):
    __tablename__ = "user_majors"

    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), primary_key=True)
    major_code = db.Column(db.String(4), db.ForeignKey("majors.code"), primary_key=True)

    user = db.relationship("User", back_populates="majors")
    major = db.relationship("Majors", back_populates="users")


class UserCourses(db.Model):
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


class Codes(db.Model):
    __tablename__ = "codes"

    code = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    registered = db.Column(db.Boolean, nullable=False)


class ApplicationStatusEnum(str, enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Applications(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), nullable=False)
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunities.id"), nullable=False
    )

    # status
    status = db.Column(
        Enum(ApplicationStatusEnum),
        nullable=False,
        default=ApplicationStatusEnum.PENDING,
    )

    resume_url = db.Column(db.String(512), nullable=True)

    applied_on = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", backref="applications")
    opportunity = db.relationship("Opportunities", backref="applications")

    # apply once per opportunity
    __table_args__ = (
        db.UniqueConstraint("user_id", "opportunity_id", name="uq_user_opportunity"),
    )


# Notification System
class NotificationTypeEnum(str, enum.Enum):
    APPLICATION_UPDATE = "application_update"
    NEW_APPLICANT = "new_applicant"
    OPPORTUNITY_MATCH = "opportunity_match"
    SYSTEM_ALERT = "system_alert"


class Notifications(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(9), db.ForeignKey("user.id"), nullable=False)

    title = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(512), nullable=False)
    notification_type = db.Column(
        Enum(NotificationTypeEnum),
        nullable=False,
        default=NotificationTypeEnum.SYSTEM_ALERT,
    )

    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    related_entity_id = db.Column(db.Integer, nullable=True)
    user = db.relationship("User", backref="notifications")
