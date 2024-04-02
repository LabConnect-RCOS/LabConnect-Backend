import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from labconnect.models import Base, RPISchools, RPIDepartments  # Import your SQLAlchemy models here

basedir = os.path.abspath(os.path.dirname(__file__))

JSON_FILE_PATH = "https://github.com/quacs/quacs-data/blob/master/semester_data/202409/schools.json"

ENGINE_URL = f"sqlite:///{os.path.join(basedir, 'database.db')}"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def load_json_data(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data

def insert_schools_and_departments(session, schools_data):
    for school_data in schools_data:
        school_name = school_data.get("name")
        school_description = "" 

        school = RPISchools(name=school_name, description=school_description)
        session.add(school)
        session.commit()
        print(f"School '{school_name}' inserted into the database.")

        for department_data in school_data.get("depts", []):
            department_code = department_data.get("code")
            department_name = department_data.get("name")
            department_description = "" 

            department = RPIDepartments(
                name=department_name,
                description=department_description,
                school_id=school_name 
            )
            session.add(department)
            session.commit()
            print(f"Department '{department_name}' inserted into the database.")

def main():
    engine = create_engine(f"sqlite:///{os.path.join(basedir, 'database.db')}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    schools_data = load_json_data(JSON_FILE_PATH)
    if not schools_data:
        print("Failed to load JSON data. Exiting...")
        return

    insert_schools_and_departments(session, schools_data)

    session.close()

if __name__ == "__main__":
    main()
