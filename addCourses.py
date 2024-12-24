import sys
from datetime import date
import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import os
import os

basedir = os.path.abspath(os.path.dirname(__file__))

from labconnect.models import Base, Courses

def fetch_json_data(json_url):
    response = requests.get(json_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch JSON data from {json_url}. Status code: {response.status_code}")
        return None

def insert_courses_from_json(session, courses_data):
    for course_code, course_info in courses_data.items():
        course_name = course_info.get('name')

        existing_course = session.query(Courses).filter_by(code=course_code).first()
        if existing_course:
            if existing_course.name != course_name:
                existing_course.name = course_name
                session.commit()
                print(f"Course '{course_code}' name updated.")
        else:
            new_course = Courses(code=course_code, name=course_name)
            session.add(new_course)
            session.commit()
            print(f"Course '{course_code}' inserted into the database.")

def main():
    engine = create_engine(f"sqlite:///{os.path.join(basedir, 'database.db')}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    json_url = "https://github.com/quacs/quacs-data/blob/master/semester_data/202409/catalog.json"
    courses_data = fetch_json_data(json_url)
    if not courses_data:
        sys.exit("Failed to fetch courses data. Exiting...")

    insert_courses_from_json(session, courses_data)
    session.close()

if __name__ == "__main__":
    main()
