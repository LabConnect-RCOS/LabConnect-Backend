from labconnect import db

# DDL

# rpi_departments( name, description ), key: name
class RPIDepartments(db.Model):
	__tablename__ = "rpi_departments"
	name = db.Column(db.String(64), primary_key=True)
	description = db.Column(db.String(256), nullable=True, unique=False)

	def __str__(self) -> str: 
		return f"{self.name}, {self.description}"

# contact_links( contact_link, contact_type ), key: contact_link
class ContactLinks(db.Model):
	__tablename__ = "contact_links"
	contact_link = db.Column(db.String(256), primary_key=True)
	contact_type = db.Column(db.String(64), nullable=True, unique=False)
	
	def __str__(self) -> str: 
		return f"{self.contact_link}, {self.contact_type}"	

# lab_runner( rcs_id, name ), key: rcs_id
class LabRunner(db.Model):
	__tablename__ = "lab_runner"
	rcs_id = db.Column(db.String(64), primary_key=True)
	name = db.Column(db.String(64), nullable=True, unique=False)

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

	def __str__(self) -> str:
		return f"{self.opp_id}, {self.name}, {self.description}, {self.active_status}, {self.recommended_experience}"

# courses( course_code, course_name ), key: course_code
class Courses(db.Model):
	__tablename__ = "courses"
	course_code = db.Column(db.String(8), primary_key=True)
	course_name = db.Column(db.String(64), nullable=True, unique=False)

	def __str__(self) -> str:
		return f"{self.course_code}, {self.course_name}"

# majors( major_code, major_name ), key: major_code
class Majors(db.Model):
	__tablename__ = "majors"
	major_code = db.Column(db.String(4), primary_key=True)
	major_name = db.Column(db.String(64), nullable=True, unique=False)

	def __str__(self) -> str:
		return f"{self.major_code}, {self.major_name}"

# class_years( class_year, class_name ), key: class_year
class ClassYears(db.Model):
	__tablename__ = "class_years"
	class_year = db.Column(db.String(64), primary_key=True)
	class_name = db.Column(db.String(64), nullable=True, unique=False)

	def __str__(self) -> str:
		return f"{self.class_year}, {self.class_name}"

# application_due_dates( date ), key: date
# class ApplicationDueDates(db.Model):


# semesters( year, season ), key: (year, season)

# salary_comp_info( usd_per_hour ), key: usd_per_hour

# upfront_pay_comp_info( usd ), key: usd

# credit_comp_info( number_of_credits, course_code ), key: (number_of_credits, course_code)

"""
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