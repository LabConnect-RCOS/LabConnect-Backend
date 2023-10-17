import sys
import random
from datetime import datetime, date, timezone

from labconnect import app, db
from labconnect.models import *

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
        		name = row_tuple[0],
        		description = row_tuple[1]
        	)
        	

        """
        for row_tuple in rpi_departments_rows: 
            row = RPIDepartments(
    	        name=row_tuple[0],
		        description=row_tuple[1]
			)
			db.session.add(row)
		"""
    	db.session.commit()

	data = db.engine.execute("SELECT * FROM rpi_departments;").scalars()
	print(data)