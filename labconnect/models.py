from labconnect import db

# DDL

# rpi_departments( name, description ), key: name
class RPIDepartments(db.Model):
	__tablename__ = "rpi_departments"
	name = db.Column(db.String(64), primary_key=True)
	description = db.Column(db.String(256), nullable=True, unique=False)

	def __str__(self) -> str: 
		return f"{self.name} {self.description}"

# DML
# I need to move DML code into its own file, then use a create app function to get the app context.
"""
with app.app_context():
	
	row = RPIDepartments(
    	name=request.form["Computer Science"],
		description=request.form["pretty cool"],
	)
	db.session.add(row)
	db.session.commit()

	data = db.engine.execute("SELECT * FROM rpi_departments;").scalars()
	print(data)

"""
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